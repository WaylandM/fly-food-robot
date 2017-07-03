# Raspberry Pi setup

## Install image
The first step is to install Adafruit's custom raspberry pi image on the micro SD card. The custom image is described here:

https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install

We want the classic version which boots into X by default, rather then the lite version that boots to the command line. The classic version can be downloaded from this link:

https://s3.amazonaws.com/adafruit-raspberry-pi/2016-10-18-pitft-28r.zip

Instructions on installing images on SD cards can be found here:

https://www.raspberrypi.org/documentation/installation/installing-images/



## Network configuration
The small screen of the pitft makes using most applications quite tricky. Therefore the first thing we should do after installing the image is configure networking, so that we can access the raspberry pi remotely using ssh.

To set a static IP address for the ethernet adapter, add the following lines to ```/etc/dhcpcd.conf```:

```
interface eth0

static ip_address=192.168.1.3/24
static routers=192.168.1.254
static domain_name_servers=192.168.1.254
```

**ip_address**, **routers** and **domain_name_servers** should be set to values appropriate for your network.

To raspberry pi can then be accessed using ssh, *e.g.*:
```
ssh pi@192.168.1.3
```

The default password for the **pi** user account is **raspberry**


## Install minicom
Minicom is useful for manual control of the robot and for editing grbl settings. To install minicom run these two commands:

```
sudo apt-get update
sudo apt-get install minicom
```

Before we can use minicom we need to enable serial:

```
sudo nano /boot/config.txt
```

Change the last line of this file from

```
enable_uart=0
```

to

```
enable_uart=1
```

Once serial is enabled we can connect to the grbl controller running on the arduino by using:

```
sudo minicom -D /dev/ttyACM0 -b115200
```

## Expand filesystem
Expand filesystem on micro SD card:

```
    sudo raspi-config
    (expand filesystem)
    sudo reboot
```

## Install robot software

Make sure you are in pi's home directory:

```
cd
```

Download and unpack robot.tar.gz

```
curl -O https://raw.githubusercontent.com/WaylandM/fly-food-robot/master/raspberrypi/robot.tar.gz
tar xzvf robot.tar.gz
```

The **robot** directory contains two subdirectories: **nc** (g-code scripts) and **py** (python scripts).

To automatically launch the robot GUI when the raspberry pi starts up, we need to edit the autostart file for the pi user:

```
sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart
```

Add the following line to autostart:

```
@/home/pi/robot/py/fly_gui.py
```
