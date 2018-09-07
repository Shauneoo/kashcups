#!/usr/bin/python
# -*- coding: utf-8 -*-

# Global variables
url = "http://192.168.1.99/kashcups/insert_nfc.php"


try:
    import RPi.GPIO as GPIO
    import time
    import requests
    
    # NFC
    import binascii
    import sys
    import Adafruit_PN532 as PN532
    


    # NFC properties
    CS   = 17
    MOSI = 23
    MISO = 24
    SCLK = 25

    # NFC constructor
    
    # Create an instance of the PN532 class.
    pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

    # Call begin to initialize communication with the PN532.  Must be done before
    # any other calls to the PN532!
    pn532.begin()    

    # Get the firmware version from the chip and print(it out.)
    ic, ver, rev, support = pn532.get_firmware_version()

    # Configure PN532 to communicate with MiFare cards.
    pn532.SAM_configuration()


    # Common functions
    
    def insert_cup(number, nfc):
        payload = {'number': number, 'nfc': nfc}
        try:
            r = requests.get(url, params=payload)
            row = int(r.text)
            if row == 1:
                print "Success!"
            elif row == -1:
                print "Error"
        except:
            print "Error reaching database"


            
    # Main Program
    while True:
        # Check if a card is available to read.
        uid = pn532.read_passive_target()
        # Try again if no card is available.
        if uid is None:
            continue
        print('Found card with UID: {0}'.format(binascii.hexlify(uid)))
        nfc = binascii.hexlify(uid)

        number = raw_input("Cup number: ")
        insert_cup(number, nfc)
        
except KeyboardInterrupt:
    GPIO.cleanup()
