# Visual Internet Tester

This repository contains a python script that pings Google repeatedly, to monitor internet connection reliability. The results are saved to a CSV file. They are also visualized on a Pimoroni Unicorn Hat Mini. A 15 pixel wide bar shows the status of each ping in real time, and two layers of different brightness are used to show older pings. Above this, a number displays the failed pings in the last 24 hours.

STL files are provided to 3D print a simple case for the device. M2 nuts and screws will be required, of length 30mm? and 5mm?. The case is intended to have a paper filter cut out and inserted as a diffuser.


Hardware:
  - Raspberry Pi Zero W
  - Pimoroni Unicorn Hat Mini
  - MicroSD card (at least 16 GB preferred)
  - Outer shell and mounting screws


Bugs:
  - After boot, system clock is wrong. It takes some time before the clock syncs automatically, and if the clock is too far off before this sync then the pings will fail. Find a way to confirm the system clock is updated before treating failures as failures.
  - When running internet-test.py in a terminal with `sudo python3 internet-test.py &`, closing the terminal causes the device to hang on a blue pending dot.

Future plans:
  - Color of the 24 hour failed pings will be based on packet loss over the last hour (1% is red?)
  - Ping bar pixels turn yellow on abnormally long response time (> 1 sec?)
  - Case will be redesigned on a slight angle for better viewing, with a shallower bezel
  - Case may include a tinted acrylic window instead of paper (or both?)
  - 24 hour display only goes to 999 -- need good solution for overflowing this
  - Google sheet support for long term data logging and analysis without needing SSH
  - A better way to set the WIFI password. Currently the only was is to SSH into the device over USB, or provide the password in a text file on the SD card


Setup instructions (maybe incomplete?):
 - Create directory in home called internet-test and copy internet-test.py, launcher.sh, and 5x7.ttf

Now install these dependencies:
```
sudo pip3 install pythonping
sudo pip3 install unicornhatmini
sudo apt install python3-pil
```
If you get `ImportError: libopenjp2.so.7`, run this:
```
sudo apt-get install libopenjp2-7-dev
```
Enable SPI:
```
sudo raspi-config nonint do_spi 0
```
Setup the launcher script:
```
@reboot sh ~/internet-test/launcher.sh >~/internet-test/logs/cronlog 2>&1
```