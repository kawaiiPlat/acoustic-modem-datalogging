#!/usr/bin/env bash

# create the venv
if [ -f venv ]
then
	echo "Creating venv"
	#python3 -m venv venv
else
	echo "venv folder exists"
fi

# activate the venv
set -e
source $PWD/venv/bin/activate

echo "Updating pip packages"
#python -m pip install -r requirements.txt

which python
