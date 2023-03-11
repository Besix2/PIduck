#!/bin/bash

sudo BRANCH=next rpi-update
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dwc2" | sudo tee -a /etc/modules
sudo echo "libcomposite" | sudo tee -a /etc/modules
chmod +x systemmd.sh
sudo reboot
