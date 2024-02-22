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
#move essential files
mv static_files/ /usr/bin/hid-gadget 
mv web_server/* /usr/bin/hid-gadget 
rm -r web_server
#installing pip
sudo apt-get install pip
#making pip available
venv_dir="/usr/bin/hid-gadget/venv"

# Check if the virtual environment already exists
if [ ! -d "$venv_dir" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$venv_dir"
fi

# Activate the virtual environment
source "$venv_dir/bin/activate"

# Install Flask if it's not already installed
if ! python -c "import flask" &> /dev/null; then
    echo "Installing Flask..."
    pip install Flask
fi
#rebooting
sudo reboot
