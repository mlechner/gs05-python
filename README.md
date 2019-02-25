# gs05-python
(still work in progress)
## dependencies
### obligatory
* python
* python-virtualenv
* libpq-dev (postgresql developer libs)
### mandatory if using Raspberry Pi Shield (RS485)  RB-RS485
* python-serial (if using Pi Shield)
* wiringpi (if using Pi Shield)
### optional packages
* libffi-dev (for lcd display support)
### recommended
* i2c-tools (for lcd display support)

## used hardware
* Raspberry Pi Model B
* RS485:
  * DIGITUS USB - Seriell Adapter (RS485) DA-70157 or
  * JOY-iT Raspberry Pi Shield (RS485)  RB-RS485
* GS05 QIS ODL-devices of the german Federal Office for Radiation Protection
  * https://odlinfo.bfs.de/DE/themen/wie-wird-gemessen/odl-sonde.html
  * https://odlinfo.bfs.de/DE/themen/wie-wird-gemessen/interpretation.html
* optional Display: JOY-iT SBC-LCD16X2
* optional: Temperatur-Sensor: JOY-iT LinkerKit Temp2 (http://www.linkerkit.de/index.php?title=LK-Temp2)

## configuration
Copy config.ini.example to config.ini to have a initial configuration.
### Section [serial]
#### device=
Device the probe is connected to. E.g. /dev/ttyS0 or /dev/ttyAMA0 (for Pi Shield RS485) or /dev/ttyUSB0 (for USB-Adapter)
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
    python run.py

## TODOS
* add more getter functions to class Records
* add Tests
* add package dependencies for optional functionalities
  * lcd
  * lk-temp2  
