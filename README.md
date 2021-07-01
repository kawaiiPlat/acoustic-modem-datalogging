# acuostic-modem-datalogging

Python scripts that are run on two Raspberry Pi 3 B+ units connected to EvoLogics acoustic modems.

## Current Objectives:
* Add comments from original Adafruit code for GPS snippets to the new scripts, credit appropriately
* Get GPIO input from the switch on the box
  * In the scripts, start a new data log file when the control switch on the box is toggled on, and stop it when it's toggled off
  * Add respective scripts to `/etc/rc.local` on both pis so it autostarts
  * Determine how the data logs will be synced/named/matched up
* Use something like sperf to get transmission stats in the lake
  * Combine with GPS Data to get sperf stats assossciated with gps points
* Develop a tool for plotting gps points on a map
