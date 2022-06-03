#!/bin/sh

cd /
cd home/pi/Software
echo "start" >> /tmp/my_script.out
sudo python3 main6.py >> /tmp/my_script.out
cd /
