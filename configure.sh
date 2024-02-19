#!/bin/bash

sudo BRANCH=next rpi-update
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt #making dwc2 available in /boot/config.txt 
echo "dwc2" | sudo tee -a /etc/modules
sudo echo "libcomposite" | sudo tee -a /etc/modules #configuring dwc2 and libcomposite as modules
#moving and giving permission to start-gadget.sh
mv start_gadget.sh /usr/bin
sudo chmod +x /usr/bin/start_gadget.sh
mv service_files/start-gadget.service /etc/systemd/system
#moving arming service
mv service_files/hid_launch_script.service /etc/systemd/system
#enable arming service
systemctl enable hid_launch_script.service
#enabling hid service
sudo systemctl enable start-gadget.service 
sudo systemctl start start-gadget.service
#giving arming script permission
sudo chmod +x arm-pi.sh
#create direcotry for script files
mkdir /usr/bin/hid-gadget
#create armed check file
touch /usr/bin/hid-gadget/armed-test.txt
#move essential files
mv static_files/. /web_server /usr/bin/hid-gadget 
#rebooting
sudo reboot
