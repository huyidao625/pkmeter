# PKMeter
<img align="right" src="media/screenshot.png">
PyQT5/Python app to display system stats and meters on your desktop. Plugin
system allows creating new meters quickly. I believe the following features
are what makes this app different from the other solutions out there:

* Quickly create new plugins with Python.
* Simple HTML template system.
* Prefrences set in the app (not cmd line scripts).

### Available Meters
* Clock
* External IP
* File System
* Google Calendar
* LmSensors
* NVIDIA
* Network
* Picasa Images
* Plex Media (recently added items)
* Plex Server (currently streaming items)
* Processes
* Sickbeard/SickRage
* Sonarr
* System Monitor
* Weather Underground
* Yahoo! Weather

### Installation (Ubuntu,Mint,Debian)
```bash
git clone https://github.com/mjs7231/pkmeter.git
cd python-pkmeter
sudo apt-get install python3-pip python3-qt5
sudo pip3 install -r requirements.pip
./pkmeter
```

### Requirements
* Python3, PyQT5
* icalendar, keyring, netifaces, plexapi, psutil, python-dateutil, xmltodict
* hg+https://mjs7231@bitbucket.org/gleb_zhulik/py3sensors

<img src="media/preferences.png">
