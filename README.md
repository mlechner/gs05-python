# gs05-python
(still work in progress)

## dependencies
* python
* python-virtualenv
* libffi-dev (for lcd display support)

## configuration



## get it running

    git clone https://github.com/mlechner/gs05-python.git
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
