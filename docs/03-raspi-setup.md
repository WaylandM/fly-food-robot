# Raspberry Pi setup

https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install

https://s3.amazonaws.com/adafruit-raspberry-pi/2016-10-18-pitft-28r.zip


https://www.raspberrypi.org/documentation/installation/installing-images/



```
    sudo raspi-config
    (expand filesystem)
    sudo reboot
```
    
/etc/dhcpcd.conf

interface eth0

static ip_address=192.168.1.3/24
static routers=192.168.1.254
static domain_name_servers=192.168.1.254

sudo apt-get update
sudo apt-get install minicom
