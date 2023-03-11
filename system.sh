#! /bin/bash
mv start_gadget /usr/bin
sudo chmod +x /usr/bin/start_gadget
new_line="/usr/bin/start_gadget"
sed -i '/fi/a '"$new_line"'' /etc/rc.local
