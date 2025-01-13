# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Random line drawing with ILI9341 TFT display.
# This is made to work with ESP8266 MicroPython and the TFT FeatherWing, but
# adjust the SPI and display initialization at the start to change boards.
# Author: Tony DiCola
# License: MIT License (https://opensource.org/licenses/MIT)
from sys import implementation
import rgbmatrix_coopmt
import adafruit_gfx.gfx
try:
    from random import randrange
except:
    import os
    def randrange(min_value, max_value):
        # Simple randrange implementation for ESP8266 os.urandom function.
        # Returns a random integer in the range min to max.  Supports only 32-bit
        # int values at most.
        magnitude = abs(max_value - min_value)
        randbytes = os.urandom(4)
        offset = int(
            (randbytes[3] << 24) | (randbytes[2] << 16) | (randbytes[1] << 8) | randbytes[0]
        )
        offset %= magnitude + 1  # Offset by one to allow max_value to be included.
        return min_value + offset

rgbPins = []
if implementation.name.upper() == "CIRCUITPYTHON":
    import board
    if hasattr(board,'MTX_ADDRA'):
        addrPins = ["MTX_ADDRA","MTX_ADDRB","MTX_ADDRC","MTX_ADDRD"]

    #    rgbPins=["MTX_R1","MTX_G1","MTX_B1","MTX_R2","MTX_G2","MTX_B2"]
    #    unused_rgbPins = None
        # for Single color (red), allows for faster refresh on slower boards
        rgbPins=["MTX_R1","MTX_R2"]
        # defining unused pins allows library to ensure noise doesn't show up as color data
        unused_rgbPins=["MTX_G1","MTX_B1","MTX_G2","MTX_B2"]
        clockPin = "MTX_CLK"
        latchPin = "MTX_LAT"
        OEPin ="MTX_OE"

# Teensy 4/4.1 pins or MicroPython
if rgbPins == []:
    addrPins = ["D21","D4","D20","D5","D3"]
    rgbPins=["D16","D1","D17","D23","D2","D22"]
    clockPin = "D19"
    latchPin = "D6"
    OEPin ="D18"
    unused_rgbPins = None
# RPi Zero2w
#    addrPins = ["D27","D25","D9","D24","D8"]
#    rgbPins=["D4","D1","D3","D2","D7","D17"]
#    clockPin = "D11"
#    latchPin = "D23"
#    OEPin ="D10"
#    unused_rgbPins = None

rows = 2 ** (len(addrPins)+1)
display = rgbmatrix_coopmt.RGBMatrix(rows,64,0,addrPins,rgbPins,clockPin,latchPin,OEPin,unused_rgbPins)

# Initialize the GFX library, giving it the display pixel function as its pixel
# drawing primitive command.
graphics = adafruit_gfx.gfx.GFX(display.rows,display.cols,display.point)

# Now loop forever drawing random lines.
display.fill(0)
while True:
    x0 = randrange(0, display.rows-1)
    y0 = randrange(0, display.cols-1)
    x1 = randrange(0, display.rows-1)
    y1 = randrange(0, display.cols-1)
    color = randrange(0, 7)
    graphics.line(x0, y0, x1, y1, color)
    display.sleep(0.01)