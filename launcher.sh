#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/internet-test
sudo systemctl daemon-reload
sudo systemctl restart systemd-timesyncd
sudo python3 internet_test.py &
cd /