#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#   Thread the operation to look for 2 cups to be simultaneously present
#   Check for 2 card then make a put request to Kash Cups server with the 2 UIDs
#
#   Once both cups are present, program will make a put request to the API and
#   then terminate
#
#   To Think About:
#
#   1. NeoPixel Statuses: currently a change in status interrupts the flow.
#   Either this is threaded or the behaviour should be trimmed to a simplistic
#   colour change


# ==============================================================================
# Imports
# ==============================================================================
import RPi.GPIO as GPIO
import time
import requests
import binascii
import sys

import binascii
import sys
import Adafruit_PN532 as PN532

from neopixel import *

import thread


# ==============================================================================
# Function definitions
# ==============================================================================

# def check_status(nfc, strip, nfc_id):
def check_status(nfc):
    payload = {'mode': '1', 'nfc': nfc}
    try:
        r = requests.get(url, params=payload)
        status = int(r.text)
        print("Current Status " + status)
        if status == 1:
            # setColor(strip, Color(255, 0, 0), nfc_id) # Green
            return 1
        elif status == 0:
            # setColor(strip, Color(0, 255, 0), nfc_id) # Red
            return 0
        else:
            # setColor(strip, Color(0, 0, 255), nfc_id) # Blue
            return 2

    except:
        # errCode(strip, Color(126, 255, 0))
        return 3


# def update_status(mode, nfc, strip):
def update_status(mode, nfc):
    payload = {'mode': mode, 'nfc': nfc}
    try:
        r = requests.get(url, params=payload)
    except:
        pass
        # errCode(strip, Color(126, 255, 0))


def insert_history(nfc1, nfc2):
    url = "http://192.168.1.99:3000/modify"  # api calls: (interaction) /modify (voting) /voting
    station_id = 'int2'  # interaction stations: [int1, int2] voting station ids: [v1a,v1b,v1c,v2a,v2b,v2c]
    operation_mode = "interaction"  # types [vote, interaction]

    payload = {'nfc1': nfc1, 'nfc2': nfc2, 'type': operation_mode,
               'station_id': station_id}

    try:
        r = requests.put(url, data=payload)
        print(r.text)
    except:
        print("Insert History Error")
        # errCode(strip, Color(0, 0, 255))


def insert_vote(nfc):
    url = "http://192.168.1.99:3000/voting"
    station_id = 'v1a'  # type: str
    operation_mode = "vote"  # type: str

    payload = {'nfc': nfc, 'type': operation_mode, 'station_id': station_id}
    try:
        r = requests.post(url, data=payload)
        print(r.text)
    except:
        print("insert vote error")
        # errCode(strip, Color(0, 0, 255))


# ==============================================================================
# NeoPixel Functions
# ==============================================================================

def colorWipe(strip, color, nfc_id=None, wait_ms=50):
     """Wipe color across display a pixel at a time."""
     if nfc_id == 1:
         for i in range(strip.numPixels() / 2):
             strip.setPixelColor(i, color)
             strip.show()
             time.sleep(wait_ms / 1000.0)
     elif nfc_id == 2:
         for i in range(strip.numPixels() / 2, strip.numPixels()):
             strip.setPixelColor(i, color)
             strip.show()
             time.sleep(wait_ms / 1000.0)
     else:
         for i in range(strip.numPixels()):
             strip.setPixelColor(i, color)
             strip.show()
             time.sleep(wait_ms / 1000.0)
#
#
# def setColor(strip, color, nfc_id=None):
#     if (nfc_id == 1):
#         for i in range(strip.numPixels() / 2):
#             strip.setPixelColor(i, color)
#             strip.show()
#     elif (nfc_id == 2):
#         for i in range((strip.numPixels() / 2), strip.numPixels()):
#             strip.setPixelColor(i, color)
#             strip.show()
#     else:
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, color)
#             strip.show()
#
#
# def theaterChase(strip, color, nfc_id=None, wait_ms=50, iterations=10):
#     """Movie theater light style chaser animation."""
#     if nfc_id == 1:
#         for j in range(iterations):
#             for q in range(3):
#                 for i in range(0, strip.numPixels() / 2, 3):
#                     strip.setPixelColor(i + q, color)
#                 strip.show()
#                 time.sleep(wait_ms / 1000.0)
#                 for i in range(0, strip.numPixels() / 2, 3):
#                     strip.setPixelColor(i + q, 0)
#     elif nfc_id == 2:
#         for j in range(iterations):
#             for q in range(3):
#                 for i in range(strip.numPixels() / 2, strip.numPixels(), 3):
#                     strip.setPixelColor(i + q, color)
#                 strip.show()
#                 time.sleep(wait_ms / 1000.0)
#                 for i in range(strip.numPixels() / 2, strip.numPixels(), 3):
#                     strip.setPixelColor(i + q, 0)
#     else:
#         for j in range(iterations):
#             for q in range(3):
#                 for i in range(0, strip.numPixels(), 3):
#                     strip.setPixelColor(i + q, color)
#                 strip.show()
#                 time.sleep(wait_ms / 1000.0)
#                 for i in range(0, strip.numPixels(), 3):
#                     strip.setPixelColor(i + q, 0)
#
#
# def wheel(pos):
#     """Generate rainbow colors across 0-255 positions."""
#     if pos < 85:
#         return Color(pos * 3, 255 - pos * 3, 0)
#     elif pos < 170:
#         pos -= 85
#         return Color(255 - pos * 3, 0, pos * 3)
#     else:
#         pos -= 170
#         return Color(0, pos * 3, 255 - pos * 3)
#
#
# def rainbow(strip, wait_ms=20, iterations=1):
#     """Draw rainbow that fades across all pixels at once."""
#     for j in range(256 * iterations):
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(i, wheel((i + j) & 255))
#         strip.show()
#         time.sleep(wait_ms / 1000.0)
#
#
# def errCode(strip, color):
#     for i in range(3):
#         setColor(strip, color)
#         time.sleep(0.5)
#         setColor(strip, Color(0, 0, 0))
#         time.sleep(0.5)
#

# ==============================================================================
# Thread Functions
# ==============================================================================

def check_for_cup_one():
    global uid1
    global tag1
    global nfc1
    global cup_one_present
    global both_cups_present

    previous_state = bool

    # while not both_cups_present:
    while True:

        uid1 = pn532a.read_passive_target()

        if uid1 is not None:
            nfc1 = binascii.hexlify(uid1)
            if nfc1 != tag1:
                print('First Tag with UID: {0}\n'.format(nfc1))
                tag1 = nfc1
                cup_one_present = True
                previous_state = True
                colorWipe(strip, Color(0, 0, 255), 1)
        else:
            cup_one_present = False

            if cup_one_present is not previous_state:
                print("Checking for First Tag\n")
                previous_state = cup_one_present
                tag1 = ""
                colorWipe(strip, Color(0, 0, 0), 1)


def check_for_cup_two():
    global uid2
    global tag2
    global nfc2
    global cup_two_present
    global both_cups_present

    previous_state = bool

    # while not both_cups_present:
    while True:

        uid2 = pn532b.read_passive_target()

        if uid2 is not None:
            nfc2 = binascii.hexlify(uid2)
            if nfc2 != tag2:
                print('Second Tag with UID: {0}\n'.format(nfc2))
                tag2 = nfc2
                cup_two_present = True
                previous_state = True
                colorWipe(strip, Color(0, 0, 255), 2)
        else:
            cup_two_present = False
            if cup_two_present is not previous_state:
                print("Checking for Second Tag\n")
                previous_state = cup_two_present
                tag2 = ""
                colorWipe(strip, Color(0, 0, 0), 2)


def clean_up_kash_cups():
    global uid1
    global uid2
    global nfc1
    global nfc2
    global tag1
    global tag2

    global cup_one_present
    global cup_two_present
    global both_cups_present

    uid1 = None
    uid2 = None
    nfc1 = None
    nfc2 = None
    tag1 = ""
    tag2 = ""

    cup_one_present = False
    cup_two_present = False
    both_cups_present = False

    colorWipe(strip, Color(0, 0, 0))

# ==============================================================================
# Globals
# ==============================================================================
uid1 = None
uid2 = None
nfc1 = None
nfc2 = None
tag1 = ""
tag2 = ""

cup_one_present = False
cup_two_present = False
both_cups_present = False

# if __name__ == "__main__":
try:

    # ==========================================================================
    # NFC properties
    # ==========================================================================
    CS1 = 17
    MOSI1 = 23
    MISO1 = 24
    SCLK1 = 25

    CS2 = 16
    MOSI2 = 20
    MISO2 = 21
    SCLK2 = 26

    # Create two instances of the PN532 class.
    pn532a = PN532.PN532(cs=CS1, sclk=SCLK1, mosi=MOSI1, miso=MISO1)
    pn532b = PN532.PN532(cs=CS2, sclk=SCLK2, mosi=MOSI2, miso=MISO2)
    pn532a.begin()
    pn532b.begin()

    # Configure PN532 to communicate with MiFare cards.
    pn532a.SAM_configuration()
    pn532b.SAM_configuration()

    # ==========================================================================
    # NeoPixel configuration
    # ==========================================================================
    LED_COUNT      = 48      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor
    # # NeoPixel constructor
    
    # # Create NeoPixel object with appropriate configuration.
    global strip 
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin() # Intialize the library (must be called once before other functions).

    # ========================================================================
    # Main Program
    # ========================================================================

    thread_one = thread
    thread_two = thread
    thread_one.start_new_thread(check_for_cup_one, ())
    thread_two.start_new_thread(check_for_cup_two, ())
    while True:
        print("waiting for both cups...\n")

        while not both_cups_present:
            if cup_one_present and cup_two_present:
                both_cups_present = True

        insert_history(nfc1, nfc2)
         
        # wait until at least 1 cup has moved
        while (cup_one_present and cup_two_present):
           colorWipe(strip, Color(255, 0, 0))
           #pass
           #time.sleep(1)
        clean_up_kash_cups()
        
        # thread_one.exit()
        # thread_two.exit()


except KeyboardInterrupt:
    GPIO.cleanup()
    # thread_one.exit()
    # thread_two.exit()
