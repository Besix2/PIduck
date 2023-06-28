<div align="center">
  <p align="center"><h1>Piduck</h1></p>
</div>


<div align="center">
  <img src="https://img.shields.io/github/issues/Besix2/PIduck" alt="GitHub open issues">
  <img src="https://img.shields.io/github/last-commit/Besix2/PIduck" alt="GitHub last commit">
  <img src="https://img.shields.io/github/commit-activity/m/Besix2/PIduck" alt="GitHub commit activity">
  <img src="https://img.shields.io/github/stars/Besix2/PIduck" alt="GitHub Repo stars">
</div>

## Description:
This project is basicly a rubber ducky but for the raspberry pi 4. It should work on all other raspberrys too and also with a little bit of modification on other Linux Distros.

## Installation:
Download the Project using
```
git clone https://github.com/Besix2/PIduck.git
```
Open it
```
cd Piduck
```
Make configure.sh and system.sh executable
```
chmod +x configure.sh
chmod +x system.sh
```
Execute configure.sh and after it finished reboot your system
```
sudo ./configure.sh
sudo reboot now
```
After Rebooting place your payload in payload.txt
```
nano payload.txt
```
Execute system.sh(WARNING: the system is now armed that means it will start uppon connection to the target machine)
```
sudo ./system.sh
```

## Usage:
When you want to change the payload simply connect the pi to your machine and change the payload.txt file(important it needs to be named payload.txt)

## To-Do
fix small bugs  
make it available for more systems  
add a local server to configure the server on the run  
add currently not working ducky features  

