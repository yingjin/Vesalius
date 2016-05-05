The software is developed for the Electronic Vesalius project that lead by John Mulligan, a lecturer at Rice University’s Humanities Research Center. 

The project presents a life-sized, acrylic model architetured by two Rice engineering students, Ben Rasich and Isaac Phillips (under supervision of Matt Wettergreen from Rice’s ODEK) and a SVG model (show on the website) contructed by John Mulligan. To know more about the project, please visit John's blog http://johncmulligan.net/blog/the-electronic-vesalius/. 

The software reacts to the physical button touch or mouse over/click of SVG on two models, lights up/hightlights the corresponding body parts to each other. Also, the application will pull data from database and show it on the website too.

The application is intended to run on a raspberry pi which connects to the physical model. However, you can run it on any platform you choose and play around with SVG model. The software is based on sqlite3, python flask, python socketio and angularjs. Please follow the instructions to install. All installation is based on Python 2.7 and assume you already have sqlite3 installed.


You need to have python-pip installed first if you don't have one.

On Linux -
>sudo apt-get update 

>sudo apt-get upgrade

>sudo apt-get install python-picamera

>sudo apt-get install python-pip


On Mac OS -
 > sudo easy_install pip


Then install virtual environment 
> pip install virtualenv

Last, run setup.sh under project top directory.
> ./setup.sh

If there is no error, you are ready to go. Activate the virtual environment
> source ./venv/bin/activate
> python vesalius.py

Check the site on 127.0.0.1:5000


