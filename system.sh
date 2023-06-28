#! /bin/bash
mv start_gadget.sh /usr/bin
sudo chmod +x /usr/bin/start_gadget.sh
new_line="/usr/bin/start_gadget.sh"
sed -i '/fi/a '"$new_line"'' /etc/rc.local
