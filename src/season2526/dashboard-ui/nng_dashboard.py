# LOOK INTO TIMER W ASYNC AND OTHER STUFF
# SPEED AND ACCELERATION COME FROM ONE PLACE, EVERYTHING ELSE FROM CAN RECEIVER

import tkinter as tk

from pynng import Pair0
import asyncio

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
PADDING = 2

addrs = {
            "speed": "tcp://127.0.0.1:5001",
            "ready": "tcp://127.0.0.1:5002",
            "radio": "tcp://127.0.0.1:5003",
            "temp": "tcp://127.0.0.1:5004",
            "acceleration": "tcp://127.0.0.1:5005",
            "charge": "tcp://127.0.0.1:5006",
            "regen_onoff": "tcp://127.0.0.1:5007",
            "regen_scale": "tcp://127.0.0.1:5008",
            "draw": "tcp://127.0.0.1:5009",
            "voltage": "tcp://127.0.0.1:5010",
        }

async def dialing(ip):
    global addrs
    s2 = Pair0(dial=ip)
    while True:
        msg = await s2.arecv()
        match ip:
            case "tcp://127.0.0.1:5001": # speed
                print(f"{msg.decode()} from {ip}")
                speed_mph.config(text=msg.decode())

            case "tcp://127.0.0.1:5002": #ready
                print(f"{msg.decode()} from {ip}")
                if(msg.decode() == "READY"):
                    rdy_status.config(text=msg.decode(), fg="green")
                else:
                    rdy_status.config(text=msg.decode(), fg="red")


            case "tcp://127.0.0.1:5003": #radio
                print(f"{msg.decode()} from {ip}")

                if(msg.decode() == "ON"):
                    radio_status.config(text=msg.decode(), fg="green")
                else:
                    radio_status.config(text=msg.decode(), fg="red")

            case "tcp://127.0.0.1:5004": #temp
                print(f"{msg.decode()} from {ip}")

                if(int(msg.decode()) > 60):
                    temp_status.config(text=f"{msg.decode()}°C", fg="red")
                elif(int(msg.decode()) > 50):
                    temp_status.config(text=f"{msg.decode()}°C", fg="orange")
                elif(int(msg.decode()) > 40):
                    temp_status.config(text=f"{msg.decode()}°C", fg="yellow")
                else:
                    temp_status.config(text=f"{msg.decode()}°C", fg="green")

            case "tcp://127.0.0.1:5005": #acceleration
                print(f"{msg.decode()} from {ip}")
                acc_status.config(text=f"{msg.decode()} m/s\u00b2")

            case "tcp://127.0.0.1:5006": #charge
                print(f"{msg.decode()} from {ip}")

                if(int(msg.decode()) > 80):
                    charge_status.config(text=msg.decode(), fg="green")
                elif (int(msg.decode()) > 50):
                    charge_status.config(text=msg.decode(), fg="yellow")
                elif (int(msg.decode()) > 25):
                    charge_status.config(text=msg.decode(), fg="orange")
                else:
                    charge_status.config(text=msg.decode(), fg="red")

            case "tcp://127.0.0.1:5007": #regen on off
                print(f"{msg.decode()} from {ip}")

                if(msg.decode() == "ON"):
                    regen_onoff_status.config(text=msg.decode(), fg="green")
                else:
                    regen_onoff_status.config(text=msg.decode(), fg="red")

            case "tcp://127.0.0.1:5008": #regen scale
                print(f"{msg.decode()} from {ip}")
                regen_scale_status.config(text=msg.decode())

            case "tcp://127.0.0.1:5009": #draw
                print(f"{msg.decode()} from {ip}")
                draw_status.config(text=msg.decode())

            case "tcp://127.0.0.1:5010": #voltage
                print(f"{msg.decode()} from {ip}")
                voltage_status.config(text=f"{msg.decode()} V")

async def tk_update_loop(interval=0.01):
     while root.winfo_exists(): 
        try:
            root.update()
        except tk.TclError:  
            break
        await asyncio.sleep(interval)

async def main():
    speed_task = asyncio.create_task(dialing(addrs["speed"]))
    ready_task = asyncio.create_task(dialing(addrs["ready"]))
    radio_task = asyncio.create_task(dialing(addrs["radio"]))
    temp_task = asyncio.create_task(dialing(addrs["temp"]))
    acceleration_task = asyncio.create_task(dialing(addrs["acceleration"]))
    charge_task = asyncio.create_task(dialing(addrs["charge"]))
    regen_onoff_task = asyncio.create_task(dialing(addrs["regen_onoff"]))
    regen_scale_task = asyncio.create_task(dialing(addrs["regen_scale"]))
    draw_task = asyncio.create_task(dialing(addrs["draw"]))
    voltage_task = asyncio.create_task(dialing(addrs["voltage"]))

    tk_task = asyncio.create_task(tk_update_loop())

    tasks = [speed_task, ready_task, radio_task, temp_task, acceleration_task, 
             charge_task, regen_onoff_task, regen_scale_task, draw_task, voltage_task,
             tk_task]

    await asyncio.gather(*tasks)

def close_window():
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()

    root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    root.configure(bg="#16191d")
    root.resizable(False, False)

    # FRAMES AND GRID SYSTEM
    spd = tk.Frame(root, bg="#1f293b", highlightbackground="#f7f8f7", highlightthickness=1)
    spd.pack_propagate(False)
    charge = tk.Frame(root, bg="#1d2126", highlightbackground="#f7f8f7", highlightthickness=1)
    charge.pack_propagate(False)
    timer = tk.Frame(root, bg="#1d2126", highlightbackground="#f7f8f7", highlightthickness=1)
    timer.pack_propagate(False)

    ready = tk.Frame(root, bg="#1d2126", highlightbackground="#f7f8f7", highlightthickness=1)
    ready.pack_propagate(False)
    regen = tk.Frame(root, bg="#1d2126", highlightbackground="#f7f8f7", highlightthickness=1)
    regen.pack_propagate(False)
    regen_scale = tk.Frame(root, bg="#1d2126", highlightbackground="#f7f8f7", highlightthickness=1)
    regen_scale.pack_propagate(False)
    radio = tk.Frame(root, bg="#1d2126", highlightbackground="#f7f8f7", highlightthickness=1)
    radio.pack_propagate(False)
    volt = tk.Frame(root, bg="#1d2126", highlightbackground="#f7f8f7", highlightthickness=1)
    volt.pack_propagate(False)
    draw = tk.Frame(root, bg="#1d2126", highlightbackground="#f7f8f7", highlightthickness=1)
    draw.pack_propagate(False)
    temp = tk.Frame(root, bg="#1d2126", highlightbackground="#f7f8f7", highlightthickness=1)
    temp.pack_propagate(False)
    acc = tk.Frame(root, bg="#1d2126", highlightbackground="#f7f8f7", highlightthickness=1)
    acc.pack_propagate(False)

    error = tk.Label(root, text="Error Here", font=("Tahqoma", 10, "bold"), bg="#1d2126", fg="red")
    error.pack_propagate(False)
    exit = tk.Button(root, text="Quit", font=("Tahqoma", 10, "bold"), bg="#1d2126", fg="red", command=close_window)

    root.columnconfigure((0,1,2,3), weight = 1)
    root.rowconfigure((0,1,2,3), weight = 1)
    root.grid_rowconfigure(4, minsize=30, weight=0)

    spd.grid(row = 0, column = 1, rowspan = 3, columnspan = 2, padx=PADDING, pady=PADDING, sticky="nsew")
    charge.grid(row = 3, column = 1, padx=PADDING, pady=PADDING, sticky="nsew")
    timer.grid(row = 3, column = 2, padx=PADDING, pady=PADDING, sticky="nsew")

    ready.grid(row = 0, column = 0, padx=PADDING, pady=PADDING, sticky = "nsew")
    regen.grid(row = 1, column = 0, padx=PADDING, pady=PADDING, sticky = "nsew")
    regen_scale.grid(row = 2, column = 0, padx=PADDING, pady=PADDING, sticky = "nsew")
    radio.grid(row = 3, column = 0, padx=PADDING, pady=PADDING, sticky = "nsew")
    volt.grid(row = 0, column = 3, padx=PADDING, pady=PADDING, sticky = "nsew")
    draw.grid(row = 1, column = 3, padx=PADDING, pady=PADDING, sticky = "nsew")
    temp.grid(row = 2, column = 3, padx=PADDING, pady=PADDING, sticky = "nsew")
    acc.grid(row = 3, column = 3, padx=PADDING, pady=PADDING, sticky = "nsew")

    error.grid(row=4, column=0, padx=PADDING, columnspan = 3, pady=PADDING, sticky = "nsew")
    exit.grid(row=4, column=3, padx=PADDING, pady=PADDING, sticky = "nsew")


    # SPEED STUFF----------------------------------------------------
    speed_label = tk.Label(
        spd,
        text="SPEED",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1f293b"
    )
    speed_label.pack()

    speed_mph = tk.Label(
        spd,
        text="-----",
        font=("Tahoma", 150, "bold"),
        fg="white",
        bg="#1f293b"
    )
    
    speed_mph.place(relx=0.5, rely=0.5, anchor="center")
    speed_mph.pack(expand=True)

    mph_sign = tk.Label(spd, text="MPH", font=("Tahoma", 20, "bold"), fg="white",
    bg="#1f293b")
    mph_sign.pack()




    # READY STUFF----------------------------------------------------
    rdy_label = tk.Label(
        ready,
        text="STATUS",
        font=("Tahoma", 10, "bold"),
        fg="white",
        bg="#1d2126"
    )
    rdy_label.pack()

    rdy_status = tk.Label(
        ready,
        text="-----",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1d2126"
    )
    rdy_status.pack()
    rdy_status.place(relx=0.5, rely=0.5, anchor="center") 


    # RADIO STATUS----------------------------------------------------
    radio_label = tk.Label(
        radio,
        text="RADIO",
        font=("Tahoma", 10, "bold"),
        fg="white",
        bg="#1d2126"
    )
    radio_label.pack()

    radio_status = tk.Label(
        radio,
        text="-----",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1d2126"
    )
    radio_status.pack()
    radio_status.place(relx=0.5, rely=0.5, anchor="center") 


    # BATTERY TEMP-----------------------------------------------------
    temp_label = tk.Label(
        temp,
        text="BATTERY TEMP",
        font=("Tahoma", 10, "bold"),
        fg="white",
        bg="#1d2126"
    )
    temp_label.pack()

    temp_status = tk.Label(
        temp,
        text="-----°C",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1d2126"
    )
    temp_status.pack()
    temp_status.place(relx=0.5, rely=0.5, anchor="center") 


    # ACCELERATION-----------------------------------------------------
    acc_label = tk.Label(
        acc,
        text="ACCELERATION",
        font=("Tahoma", 10, "bold"),
        fg="white",
        bg="#1d2126"
    )
    acc_label.pack()

    acc_status = tk.Label(
        acc,
        text="----- m/s\u00b2",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1d2126"
    )
    acc_status.pack()
    acc_status.place(relx=0.5, rely=0.5, anchor="center") 


    # CHARGE------------------------------------------------------------
    charge_label = tk.Label(
        charge,
        text="CHARGE",
        font=("Tahoma", 10, "bold"),
        fg="white",
        bg="#1d2126"
    )
    charge_label.pack()

    charge_status = tk.Label(
        charge,
        text="-----",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1d2126"
    )
    charge_status.pack()
    charge_status.place(relx=0.5, rely=0.5, anchor="center") 


    # TIMER------------------------------------------------------------
    time_label = tk.Label(
        timer,
        text="TIME ELAPSED",
        font=("Tahoma", 10, "bold"),
        fg="white",
        bg="#1d2126"
    )
    time_label.pack()

    time_status = tk.Label(
        timer,
        text=f"00:00.000",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1d2126"
    )
    time_status.pack()
    time_status.place(relx=0.5, rely=0.5, anchor="center") 


    # REGEN ON / OFF-------------------------------------------------------
    regen_onoff_label = tk.Label(
        regen,
        text="REGEN STATUS",
        font=("Tahoma", 10, "bold"),
        fg="white",
        bg="#1d2126"
    )
    regen_onoff_label.pack()

    regen_onoff_status = tk.Label(
        regen,
        text="-----",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1d2126"
    )
    regen_onoff_status.pack()
    regen_onoff_status.place(relx=0.5, rely=0.5, anchor="center") 

    #REGEN SCALE---------------------------------------------
    regen_scale_label = tk.Label(
        regen_scale,
        text="REGEN SCALE",
        font=("Tahoma", 10, "bold"),
        fg="white",
        bg="#1d2126"
    )
    regen_scale_label.pack()

    regen_scale_status = tk.Label(
        regen_scale,
        text="-----",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1d2126"
    )
    regen_scale_status.pack()
    regen_scale_status.place(relx=0.5, rely=0.5, anchor="center") 


    #DRAW---------------------------------------------
    draw_label = tk.Label(
        draw,
        text="DRAW",
        font=("Tahoma", 10, "bold"),
        fg="white",
        bg="#1d2126"
    )
    draw_label.pack()

    draw_status = tk.Label(
        draw,
        text="-----",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1d2126"
    )
    draw_status.pack()
    draw_status.place(relx=0.5, rely=0.5, anchor="center") 



    # VOLTAGE --------------------------------------------------
    voltage_label = tk.Label(
        volt,
        text="VOLTAGE",
        font=("Tahoma", 10, "bold"),
        fg="white",
        bg="#1d2126"
    )
    voltage_label.pack()

    voltage_status = tk.Label(
        volt,
        text="----- V",
        font=("Tahoma", 20, "bold"),
        fg="white",
        bg="#1d2126"
    )
    voltage_status.pack()
    voltage_status.place(relx=0.5, rely=0.5, anchor="center") 


    asyncio.run(main()) 
