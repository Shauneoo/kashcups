# Kashcups V2
Kashcups V2 is a project that tracks social interactions and votes on social questions.

## Getting Started

This project consists of three parts:

* kashcupAPI (API handling db updating)
* kashcupAPP (react app for displaying data)
* Code on RFID readers (python scripts for reading nfc tags and sending data)


## Prerequisites
You'll need the following for the project:  
* sql Database  
* node  
* rfid readers based on Raspberry Pi platform.  


## Installing
Installation instructions for kashcupAPI, kashcupAPP, Code on RFID readers  

Download or clone repository to your local machine.  
`git clone https://github.com/Shauneoo/kashcups.git`

cd into Kashcups folder  
`cd kashcups`

###kashcupAPI
Installing the API portion of Kashcups  

cd into Kashcups API folder  
`cd kashcupAPI`

install node_modules  
`npm install` or `yarn install`

start API  
`node app.js` or `yarn app.js`

###kashcupAPP
Installing the APP portion of Kashcups  

cd into kashcupAPP repository  
`cd kashcupAPP`

install node_modules  
`npm install` or `yarn install`

start APP  
`npm start` or `yarn start`

If the API script is running you'll be prompted to select an alternative port.  
`y`

A web browser will open to show the node app.  

###Reader Code
Installing the reader code portion of Kashcups  

On a fresh install on a raspberry pi.  
`sudo apt-get update` & `sudo apt-get upgrade`

Install needed libraries  
1. `sudo apt-get install build-essential python-dev git`  
2. `sudo apt-get update`  
3. `sudo apt-get install python-requests scons swig`  
4. Install PN532 library
`sudo apt-get update`  
`sudo apt-get install build-essential python-dev git`  
`git clone https://github.com/adafruit/Adafruit_Python_PN532.git`  
`cd Adafruit_Python_PN532`  
`sudo python setup.py install`  
5. Install rpi_ws281x Library  
`git clone https://github.com/jgarff/rpi_ws281x.git`  
`cd rpi_ws281x`  
`scons`  
`cd python`  
`sudo python setup.py install`  

Configure the config of the reader depending on reader type.

For Voting stations:  
`url = "http://192.168.1.99:3000/voting"
station_id = 'v1a'
type = "vote"`  

Possible Voting station id's [v1a,v1b,v1c,v2a,v2b,v2c]  

For Interaction stations:  
`url = "http://192.168.1.99:3000/modify"
station_id = 'int1'
type = "interaction" `  

Possible Interaction station id's [int1, int2]  

Run the corresponding code for the reader type.  
Voting station `sudo python single_nfc.py`  Or  
Interaction station `sudo python double_nfc.py`

##Deployment

###How to get points for #ID
1. log onto network KashCupsNetwork
2. Credentials: -n `KashCupsNetwork` -p `kashcups`
3. Open web browser
4. Navigate to `192.168.1.99`
5. Click on Kashcups logo image.
6. Enter #ID

## Authors
V2  
* **Shaune Oosthuizen** - *V2 Main Author* - [Shauneoo](https://github.com/Shauneoo/)
* **Jonathan Rankin** - *V2 Contributor* - [rankinjonathan](https://github.com/rankinjonathan)
V1  
* **Ferdinand Andre Ginting Munthe** - *V1 Initial author*
* **Edson Alcalá** - *V1 Contributor* - [EdsonAlcala](https://github.com/EdsonAlcala)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
