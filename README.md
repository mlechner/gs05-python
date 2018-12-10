# gs05-python
(still work in progress)
## dependencies
* python
* python-virtualenv
* libffi-dev (for lcd display support)
## used hardware
* Raspberry Pi Model B
* RS485:
  * DIGITUS USB - Seriell Adapter (RS485) DA-70157 or
  * JOY-IT Raspberry Pi Shield (RS485 )  RB-RS485
* GS05 QIS ODL-devices of the german Federal Office for Radiation Protection
  * https://odlinfo.bfs.de/DE/themen/wie-wird-gemessen/odl-sonde.html
  * https://odlinfo.bfs.de/DE/themen/wie-wird-gemessen/interpretation.html
* optional Display: JOY-IT SBC-LCD16X2
## configuration
Copy config.ini.example to config.ini to have a initial configuration.
### Section [serial]
#### device=
Device the probe is cionnected to. E.g. /dev/ttyAMA0 or /dev/ttyUSB0
#### serial parameters
baudrate=9600  
bytesize=8  
parity=N  
stopbits=1  
timeout=1
#### receivekey=
Key sent to request collected data from the probe 
#### deviceid
Custom string to set the id of the probe, e.g. 1234Q, because the probes do not have an identifier in there sent data.
### Section [lcd]
#### lcd=
1 to activate LCD support, empty for OFF
#### valueout=
Linenumber on the LCD display the measured values will be sent to. E.g. 2
#### timestamp=
Linenumber on the LCD display a timestamp will be sent to. E.g. 1. Empty if no timestamp shall be displayed (e.g. if a second device uses line 1.)
### Section [polling]
Configure the data request  
FIXME "receivekey should be moved to here"
#### waittime=
Seconds to wait for next data request. E.g. 60
#### repeat=
Number of duplicate Lines sent by the probe on data request. E.g. 3. this is used to detect transmission errors.
### Section [db]
#### driver=
Which DB backend to use. Supported: sqlite, postgresql
#### sqlite=
SQLite connection string e.g.
sqlite:///records.sqlite
#### postgresql connection parameters
host=localhost  
port=5432  
database=gs05  
user=postgres  
pass=pass

## get it running
    git clone --recursive https://github.com/mlechner/gs05-python.git
    cd gs05-python
    # adapt config.ini to your needs
    cp config.ini.example config.ini
    virtualenv venv
    source venv/bin/activate
    pip install --upgrade pip
    # for lcd display support
    pip install smbus-cffi
    # mandatory steps
    pip install .
    python schema.py # to create sqlite DB
    python run.py
