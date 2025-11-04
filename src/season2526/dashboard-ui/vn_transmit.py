import os
import sys
import math
import asyncio

from pynng import Pair0

try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

try:
    from vectornav import Registers, Sensor
except Exception as e:
    print("VectorNav SDK is not installed. Install the VectorNav Python SDK to use vn_transmit.")
    raise


ACCEL_ADDR = "tcp://127.0.0.1:5005"


def get_com_port() -> str:
    """Load COM_PORT, handling Windows UTF-16 .env files gracefully."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")

    # Try python-dotenv first with UTF-8; if BOM/encoding error occurs, retry as UTF-16
    if load_dotenv is not None and os.path.exists(env_path):
        try:
            load_dotenv(dotenv_path=env_path)
        except UnicodeDecodeError:
            try:
                load_dotenv(dotenv_path=env_path, encoding="utf-16")
            except Exception:
                pass

    # Fallback: manual parse if still not present
    com_port = os.getenv("COM_PORT")
    if not com_port and os.path.exists(env_path):
        try:
            with open(env_path, "rb") as f:
                data = f.read()
            # Detect UTF-16LE BOM (FF FE) or UTF-16BE (FE FF)
            if data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff"):
                try:
                    text = data.decode("utf-16")
                except Exception:
                    text = ""
            else:
                try:
                    text = data.decode("utf-8")
                except Exception:
                    # Last resort: system default
                    text = data.decode(errors="ignore")
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.upper().startswith("COM_PORT="):
                    com_port = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
        except Exception:
            pass

    return com_port or "COM3"


async def publish_acceleration(sensor: "Sensor") -> None:
    sock_accel = Pair0(listen=ACCEL_ADDR)

    binary_output_cfg = Registers.System.BinaryOutput1()
    binary_output_cfg.asyncMode.serial1 = 1
    binary_output_cfg.asyncMode.serial2 = 1
    binary_output_cfg.rateDivisor = 400
    binary_output_cfg.common.timeStartup = 1
    binary_output_cfg.common.accel = 1
    binary_output_cfg.common.angularRate = 1
    binary_output_cfg.common.imu = 1

    sensor.writeRegister(binary_output_cfg)

    while True:
        composite_data = sensor.getNextMeasurement()
        if not composite_data:
            await asyncio.sleep(0)
            continue

        if composite_data.matchesMessage(binary_output_cfg):
            # Print packet details similar to vn_template
            try:
                print("Found binary 1 measurement.")
                try:
                    time_startup = composite_data.time.timeStartup.nanoseconds()
                    print(f"\tTime: {time_startup}")
                except Exception:
                    pass
                accel = composite_data.imu.accel
                ax, ay, az = float(accel[0]), float(accel[1]), float(accel[2])
                print(f"\tAccel X: {ax}\n\tAccel Y: {ay}\n\tAccel Z: {az}")

                magnitude = math.sqrt(ax * ax + ay * ay + az * az)
                msg = f"{magnitude:.2f}".encode()
                await sock_accel.asend(msg)
            except Exception:
                # If parsing fails, skip but keep loop alive
                pass
        elif composite_data.matchesMessage("VNYPR"):
            try:
                print("Found ASCII YPR measurement.")
                ypr = composite_data.attitude.ypr
                print(f"\tYaw: {ypr.yaw}\n\tPitch: {ypr.pitch}\n\tRoll: {ypr.roll}")
            except Exception:
                pass
        else:
            print("Unrecognized asynchronous message received")
            await asyncio.sleep(0)


async def amain() -> None:
    # Match vn_template style: allow argv override, default to COM3 or .env
    port_name = sys.argv[1] if len(sys.argv) > 1 else get_com_port()

    sensor = Sensor()
    try:
        sensor.autoConnect(port_name)
    except Exception as latest_error:
        print(f"Error: {latest_error} while connecting to {port_name}.")
        return

    # Configure ADOR/ADOF similar to vn_template for completeness
    try:
        async_type = Registers.System.AsyncOutputType()
        async_type.ador = Registers.System.AsyncOutputType.Ador.YPR
        async_type.serialPort = Registers.System.AsyncOutputType.SerialPort.Serial1
        sensor.writeRegister(async_type)

        async_freq = Registers.System.AsyncOutputFreq()
        async_freq.adof = Registers.System.AsyncOutputFreq.Adof.Rate2Hz
        async_freq.serialPort = Registers.System.AsyncOutputFreq.SerialPort.Serial1
        sensor.writeRegister(async_freq)
    except Exception:
        # Non-fatal; continue with binary output streaming
        pass

    try:
        await publish_acceleration(sensor)
    except asyncio.CancelledError:
        pass
    except KeyboardInterrupt:
        pass
    finally:
        try:
            sensor.disconnect()
        except Exception:
            pass


def main() -> None:
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()


