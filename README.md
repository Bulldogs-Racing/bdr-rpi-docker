# bdr-rpi-docker repository manual

## About this repository
This is the documentation for the GitHub repository called bdr-rpi-docker. It is a Docker environment designed to be integrated with Visual Studios Code for the simulation of the Raspberry Pi environment that the Bulldog’s Racing car operates on. This was designed for development purposes.

## Who should use this docker environment?
Anyone who wishes to familiarize themselves with Raspberry Pi and wants the basic file tree there already.
A general knowledge of UNIX is helpful, but not required.

## Software requirements (Windows 10/11) 
-	Install Docker Desktop
-	When prompted, install WSL. An acronym for Windows Subsystem for Linux, it allows Docker to run on your Windows system. Please note this will create a partition, but it is also easy to uninstall so do not fret.

## Quickstart 
0)	VERY IMPORTANT: do software requirements FIRST
1)	Navigate to the repository page on Github bdr-rpi-docker. MAKE SURE THE BRANCH IS “windows-release” NOT main.
2)	Expand folder, and open in Visual Studios code (download here) 
3)	Install the Container tools extension by Microsoft in VSCode
4)	In VS Code, press CNTRL+SHIFT+P and type reopen in container

## Theory
### What is Docker?
Docker is an open platform that enables developers to build, ship, and run applications within isolated environments called containers. It achieves this by providing a standardized way to package an application and all its dependencies (libraries, system tools, code, and runtime) into a single, self-contained unit.
