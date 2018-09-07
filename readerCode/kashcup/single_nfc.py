#!/usr/bin/python
# -*- coding: utf-8 -*-

# Global variables
url = "http://192.168.1.99/kashcups/single_nfc.php"
station_id = 1
tag = ""
stat=0;

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
    CS   = 17
    MOSI = 23
    MISO = 24
    SCLK = 25

    #NeoPixel configuration
    LED_COUNT      = 24      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor 

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

    
    # NeoPixel constructor

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    
    # Common functions
    def check_status(nfc, strip):
        payload = {'mode': '1', 'nfc': nfc}
        try:
            r = requests.get(url, params=payload)
            status = int(r.text)
            if status == 1:
                setColor(strip, Color(255, 0, 0)) # Green
                return 1
            elif status == 0:
                setColor(strip, Color(0, 255, 0)) # Red
                return 0
            else:
                theaterChase(strip, Color(0, 0, 255)) # Blue
                return 2

        except:
            errCode(strip, Color(0, 0, 255))
            return 3

    def update_status(mode, nfc, strip):
        payload = {'mode': mode, 'nfc': nfc}
        try:
            r = requests.get(url, params=payload)
        except:
            errCode(strip, Color(0, 0, 255))

    def insert_history(nfc, type, station_id, strip):
	payload = {'mode': '5', 'nfc1': nfc, 'type': type, 'station_id': station_id}
	try:
	    r = requests.get(url, params=payload)
	except:
	    errCode(strip, Color(0, 0, 255))

    # NeoPixel functions
    def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms/1000.0)

    def setColor(strip, color):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()

    def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
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
        uid = pn532.read_passive_target()
        # Try again if no card is available.
        if uid is None:
            setColor(strip, Color(0, 0, 0)) # Off
            tag = ""
            continue
        #print('Found card with UID: {0}'.format(binascii.hexlify(uid)))
        nfc = binascii.hexlify(uid)

        if (tag != nfc):
            stat = check_status(nfc, strip)
            print nfc
            print stat
            if stat == 1:
                time.sleep(0.7) # Delay for green color
                update_status(3, nfc, strip)
                colorWipe(strip, Color(0, 255, 0)) # Red
                check_status(nfc, strip)
		insert_history(nfc, 0, station_id, strip)
            tag = nfc

except KeyboardInterrupt:
    GPIO.cleanup()
