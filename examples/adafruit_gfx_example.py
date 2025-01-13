# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test of primitive drawing with ILI9341 TFT display.
# This is made to work with ESP8266 MicroPython and the TFT FeatherWing, but
# adjust the SPI and display initialization at the start to change boards.
# Author: Tony DiCola
# License: MIT License (https://opensource.org/licenses/MIT)
from sys import implementation
import rgbmatrix_coopmt
import adafruit_gfx.gfx

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

rows = 2 ** (len(addrPins)+1)
display = rgbmatrix_coopmt.RGBMatrix(rows,64,0,addrPins,rgbPins,clockPin,latchPin,OEPin,unused_rgbPins)

# Initialize the GFX library, giving it the display pixel function as its pixel
# drawing primitive command.
graphics = adafruit_gfx.gfx.GFX(display.rows,display.cols,display.point)

# Set to False to reduce flicker esp on slower driver boards
refreshslow = True
# Now loop forever drawing different primitives.

if len(rgbPins) == 6:
    red = 5
    green = 2
    blue = 1
    pink = 5
else:
    red = 1
    green = 1
    blue = 1
    pink = 1

while True:
    # Clear screen and draw a red line.
    display.fill(0)
    graphics.line(0, 0, display.rows-1, display.cols-1, red)
    display.sleep(2,refreshslow)
    # Clear screen and draw a green rectangle.
    display.fill(0)
    graphics.rect(0, 0, display.rows//2, display.cols//2, green)
    display.sleep(2,refreshslow)
    # Clear screen and draw a filled green rectangle.
    display.fill(0)
    graphics.fill_rect(0, 0, display.rows//2, display.cols//2, green)
    display.sleep(2,refreshslow)
    # Clear screen and draw a blue circle.
    display.fill(0)
    graphics.circle(display.rows//2, display.cols//2,
        min(display.rows,display.cols)//4, blue)
    display.sleep(2,refreshslow)
    # Clear screen and draw a filled blue circle.
    display.fill(0)
    graphics.fill_circle(display.rows//2, display.cols//2, 
        min(display.rows,display.cols)//4, blue)
    display.sleep(2,refreshslow)
    # Clear screen and draw a pink triangle.
    display.fill(0)
    graphics.triangle(display.rows//2, display.cols//3, 
        round(display.rows/1.333), round(display.cols/1.75), 
        display.rows//4, round(display.cols/1.75), pink)
    display.sleep(2,refreshslow)
    # Clear screen and draw a filled pink triangle.
    display.fill(0)
    graphics.fill_triangle(display.rows//2, display.cols//3, 
        round(display.rows/1.333), round(display.cols/1.75), 
        display.rows//4, round(display.cols/1.75), pink)
    display.sleep(2,refreshslow)