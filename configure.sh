#!/bin/bash

sudo BRANCH=next rpi-update
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt #making dwc2 available in /boot/config.txt 
echo "dwc2" | sudo tee -a /etc/modules
sudo echo "libcomposite" | sudo tee -a /etc/modules #configuring dwc2 and libcomposite as modules
#moving and giving permission to start-gadget.sh
mv start_gadget.sh /usr/bin
sudo chmod +x /usr/bin/start_gadget.sh
mv start-gadget.service /etc/systemd/system
#enabling hid service
sudo systemctl enable start-gadget.service 
sudo systemctl start start-gadget.service
sudo reboot
