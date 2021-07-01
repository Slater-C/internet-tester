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
  - Investigate whether unplugging the device during a write to the CSV could corrupt it, and create a failsafe.

Future plans:
  - Color of the 24 hour failed pings will be based on packet loss over the last hour (1% is red?)
  - Ping bar pixels turn yellow on abnormally long response time (> 1 sec?)
  - Case will be redesigned on a slight angle for better viewing, with a shallower bezel
  - Case may include a tinted acrylic window instead of paper (or both?)
  - 24 hour display only goes to 999 -- need good solution for overflowing this
  - Better CSV formatting, and separation of CSV into files based on week
  - Maybe a local web page capable of graphing the last week of results, and allowing a download of the CSV for longer term logs
  - A better way to set the WIFI password. Currently the only was is to SSH into the device over USB, or provide the password in a text file on the SD card

  - Setup instructions
