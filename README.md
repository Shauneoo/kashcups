

##installing on pi
fresh install on pi
update pi
`sudo apt-get update`
`sudo apt-get upgrade`

install prerequesits
`sudo apt-get install build-essential python-dev git install python-requests scons swig`

install libaries code libraries

Install PN532 library
`sudo apt-get update
sudo apt-get install build-essential python-dev git
git clone https://github.com/adafruit/Adafruit_Python_PN532.git
cd Adafruit_Python_PN532
sudo python setup.py install`

Install rpi_ws281x Library
`git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install
`
