#!/bin/bash


pip install virtualenv


# This part uses virtualenv to create a localized python configuration

if [ ! -d venv  ]; then
	virtualenv --no-site-packages -p /usr/bin/python2.7 venv
fi

. venv/bin/activate

pip install -r requirements.txt