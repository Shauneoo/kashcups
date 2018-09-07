#!/usr/bin/python
# -*- coding: utf-8 -*-

# Global variables
url = "http://192.168.1.99/kashcups/single_nfc.php"
tag1 = ""
tag2 = ""
stat1=-1
stat2=-1


try:
    import RPi.GPIO as GPIO
    import time
    import requests
    
    # NFC
    import binascii
    import sys
    import Adafruit_PN532 as PN532
    
    #NeoPixel Ring
    from neopixel import *

    # NFC properties
    CS1   = 17
    MOSI1 = 23
    MISO1 = 24
    SCLK1 = 25

    CS2   = 16
    MOSI2 = 20
    MISO2 = 21
    SCLK2 = 26
    
    #NeoPixel configuration
    LED_COUNT      = 48      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor 

    # NFC constructor
    
    # Create two instances of the PN532 class.
    pn532a = PN532.PN532(cs=CS1, sclk=SCLK1, mosi=MOSI1, miso=MISO1)
    pn532b = PN532.PN532(cs=CS2, sclk=SCLK2, mosi=MOSI2, miso=MISO2)

    # Call begin to initialize communication with the PN532.  Must be done before
    # any other calls to the PN532!
    pn532a.begin()
    pn532b.begin()

    # Get the firmware version from the chip and print(it out.)
    #ic1, ver1, rev1, support1 = pn532a.get_firmware_version()
    #ic2, ver2, rev2, support2 = pn532b.get_firmware_version()
    #print('Found PN532a with firmware version: {0}.{1}'.format(ver1, rev1))
    #print('Found PN532b with firmware version: {0}.{1}'.format(ver2, rev2))

    # Configure PN532 to communicate with MiFare cards.
    pn532a.SAM_configuration()
    pn532b.SAM_configuration()

    
    # NeoPixel constructor

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    
    # Common functions
    def check_status(nfc, strip, nfc_id):
        payload = {'mode': '1', 'nfc': nfc}
        try:
            r = requests.get(url, params=payload)
            status = int(r.text)
            if status == 1:
                setColor(strip, Color(255, 0, 0), nfc_id) # Green
                return 1
            elif status == 0:
                setColor(strip, Color(0, 255, 0), nfc_id) # Red
                return 0
            else:
                setColor(strip, Color(0, 0, 255), nfc_id) # Blue
                return 2

        except:
            errCode(strip, Color(126, 255, 0))
            return 3

    def update_status(mode, nfc, strip):
        payload = {'mode': mode, 'nfc': nfc}
        try:
            r = requests.get(url, params=payload)
        except:
            errCode(strip, Color(126, 255, 0))

    # NeoPixel functions
    def colorWipe(strip, color, nfc_id=None, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
        if nfc_id == 1:
            for i in range(strip.numPixels()/2):
                strip.setPixelColor(i, color)
                strip.show()
                time.sleep(wait_ms/1000.0)
        elif nfc_id == 2:
            for i in range(strip.numPixels()/2, strip.numPixels()):
                strip.setPixelColor(i, color)
                strip.show()
                time.sleep(wait_ms/1000.0)
        else:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
                strip.show()
                time.sleep(wait_ms/1000.0)            

    def setColor(strip, color, nfc_id=None):
        if (nfc_id == 1):
            for i in range(strip.numPixels()/2):
                strip.setPixelColor(i, color)
                strip.show()
        elif (nfc_id == 2):
            for i in range((strip.numPixels()/2), strip.numPixels()):
                strip.setPixelColor(i, color)
                strip.show()
        else:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
                strip.show()
                
    def theaterChase(strip, color, nfc_id=None, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	if nfc_id == 1:
            for j in range(iterations):
                for q in range(3):
                    for i in range(0, strip.numPixels()/2, 3):
                        strip.setPixelColor(i+q, color)
                    strip.show()
                    time.sleep(wait_ms/1000.0)
                    for i in range(0, strip.numPixels()/2, 3):
                        strip.setPixelColor(i+q, 0)
        elif nfc_id == 2:
            for j in range(iterations):
                for q in range(3):
                    for i in range(strip.numPixels()/2, strip.numPixels(), 3):
                        strip.setPixelColor(i+q, color)
                    strip.show()
                    time.sleep(wait_ms/1000.0)
                    for i in range(strip.numPixels()/2, strip.numPixels(), 3):
                        strip.setPixelColor(i+q, 0)
        else:
            for j in range(iterations):
                for q in range(3):
                    for i in range(0, strip.numPixels(), 3):
                        strip.setPixelColor(i+q, color)
                    strip.show()
                    time.sleep(wait_ms/1000.0)
                    for i in range(0, strip.numPixels(), 3):
                        strip.setPixelColor(i+q, 0)            

    def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
	else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)
	    
    def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
            for i in range(strip.numPixels()):
		strip.setPixelColor(i, wheel((i+j) & 255))
	    strip.show()
	    time.sleep(wait_ms/1000.0)

    def errCode(strip, color):
        for i in range(3):
            setColor(strip, color)
            time.sleep(0.5)
            setColor(strip, Color(0, 0, 0))
            time.sleep(0.5)

            
    # Main Program
    rainbow(strip)  # Initialisation
    setColor(strip, Color(0, 0, 0)) # Off
    while True:
        
        # Check if a card is available to read.
        uid1 = pn532a.read_passive_target()
        # Try again if no card is available.
        if uid1 is None:
            setColor(strip, Color(0, 0, 0), 1) # Off
            tag1 = ""
            stat1 = -1
            #continue
        #print('Found card with UID: {0}'.format(binascii.hexlify(uid)))
        else:
            nfc1 = binascii.hexlify(uid1)

            if (tag1 != nfc1):
                stat1 = check_status(nfc1, strip, 1)
                print nfc1
                print stat1
                #if stat1 == 1:
                    #time.sleep(0.7) # Delay for green color
                    #colorWipe(strip, Color(0, 255, 0)) # Red
                    #update_status(3, nfc1, strip)
                    #check_status(nfc1, strip)
                tag1 = nfc1
        
        # Check if a card is available to read.
        uid2 = pn532b.read_passive_target()
        # Try again if no card is available.
        if uid2 is None:
            setColor(strip, Color(0, 0, 0), 2) # Off
            tag2 = ""
            stat2 = -1
            #continue
        #print('Found card with UID: {0}'.format(binascii.hexlify(uid)))
        else:
            nfc2 = binascii.hexlify(uid2)            

            if (tag2 != nfc2):
                stat2 = check_status(nfc2, strip, 2)
                print nfc2
                print stat2
                #if stat2 == 1:
                    #time.sleep(0.7) # Delay for green color
                    #colorWipe(strip, Color(0, 255, 0)) # Red
                    #update_status(3, nfc2, strip)
                    #check_status(nfc2, strip)
                tag2 = nfc2
                
        # Turn into on
        if (((stat1 == 0) | (stat2 == 0)) & ((stat1 != -1) & (stat2 != -1)) ):
            if (stat1 != 2) & (stat2 != 2):
                if stat1 == 0:
                    time.sleep(0.7) # Delay for red color
                    update_status(2, nfc1, strip)
                    colorWipe(strip, Color(255, 0, 0), 1) # Green
                    stat1 = -1
                if stat2 == 0:
                    time.sleep(0.7) # Delay for red color
                    update_status(2, nfc2, strip)
                    colorWipe(strip, Color(255, 0, 0), 2) # Green
                    stat2 = -1
                
            
except KeyboardInterrupt:
    GPIO.cleanup()
