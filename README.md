# acuostic-modem-datalogging

Python scripts that are run on two Raspberry Pi 3 B+ units connected to EvoLogics acoustic modems.

# In Progress: setting up a python venv to make testing easier
* To set up a new device, use `./setup.sh`, which will create a venv for you and pull the requirements.txt with pip
* Activate the venv with `source venv/bin/activate`
* Run your code
* Deactivate with `deactivate`

## Current Objectives:
* Add comments from original Adafruit code for GPS snippets to the new scripts, credit appropriately
* Get GPIO input from the switch on the box
  * In the scripts, start a new data log file when the control switch on the box is toggled on, and stop it when it's toggled off
  * Add respective scripts to `/etc/rc.local` on both pis so it autostarts
  * Determine how the data logs will be synced/named/matched up
* Use something like [sperf](https://github.com/sandyUni/sPerf) to get transmission stats in the lake
  * Combine with GPS Data to get sperf stats assossciated with gps points
* Develop a tool for plotting gps points on a map
