# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test of primitive drawing with ILI9341 TFT display.
# This is made to work with ESP8266 MicroPython and the TFT FeatherWing, but
# adjust the SPI and display initialization at the start to change boards.
# Author: Tony DiCola
# License: MIT License (https://opensource.org/licenses/MIT)
from sys import implementation
import rgbmatrix_coopmt

rgbPins = []
if implementation.name.upper() == "CIRCUITPYTHON":
    import board
    if hasattr(board,'MTX_ADDRA'):
        addrPins = ["MTX_ADDRA","MTX_ADDRB","MTX_ADDRC","MTX_ADDRD"]

        rgbPins=["MTX_R1","MTX_G1","MTX_B1","MTX_R2","MTX_G2","MTX_B2"]
        unused_rgbPins = None
        # for Single color (red), allows for faster refresh on slower boards
#        rgbPins=["MTX_R1","MTX_R2"]
        # defining unused pins allows library to ensure noise doesn't show up as color data
#        unused_rgbPins=["MTX_G1","MTX_B1","MTX_G2","MTX_B2"]
        clockPin = "MTX_CLK"
        latchPin = "MTX_LAT"
        OEPin ="MTX_OE"

# Teensy 4/4.1 pins or MicroPython
if rgbPins == []:
#    addrPins = ["D21","D4","D20","D5","D3"]
#    rgbPins=["D16","D1","D17","D23","D2","D22"]
#    clockPin = "D19"
#    latchPin = "D6"
#    OEPin ="D18"
#    unused_rgbPins = None

# RPi Zero2w
    addrPins = ["D27","D25","D9","D24","D8"]
    rgbPins=["D4","D1","D3","D2","D7","D17"]
    clockPin = "D11"
    latchPin = "D23"
    OEPin ="D10"
    unused_rgbPins = None

rows = 2 ** (len(addrPins)+1)
display = rgbmatrix_coopmt.RGBMatrix(rows,64,addrPins,rgbPins,clockPin,latchPin,OEPin,unused_rgbPins)

# Set to True to reduce flicker especially on slower driver boards
optimize = False
# Option to animate the area fills
animate = True
# Now loop forever drawing different primitives.

if len(rgbPins) == 6:
    red = 4
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
    display.line(0, 0, display.rows-1, display.cols-1, red)
    display.sleep(2,optimize)
    # Clear screen and draw a green rectangle.
    display.fill(0)
    points = [[0,0],[0,display.cols//2],
        [display.rows//2,display.cols//2],[display.rows//2,0]]
    display.polygon(points, green)
    display.sleep(2,optimize)
    # Clear screen and draw a filled green rectangle.
    #display.fill(0)
    display.fillarea(display.rows//4,display.cols//4,green,animate,optimize)
    display.sleep(2,optimize)
    # Clear screen and draw a blue circle.
    display.fill(0)
    display.circle(display.rows//2, display.cols//2,
        min(display.rows,display.cols)//4, blue)
    display.sleep(2,optimize)
    # Clear screen and draw a filled blue circle.
    display.fillarea(display.rows//2, display.cols//2, blue,animate,optimize)
    display.sleep(2,optimize)
    # Clear screen and draw a pink triangle.
    display.fill(0)
    points = [[display.rows//2, display.cols//3], 
        [round(display.rows/1.333), round(display.cols/1.75)], 
        [display.rows//4, round(display.cols/1.75)]]
    display.polygon(points, pink)
    display.sleep(2,optimize)
    # Clear screen and draw a filled pink triangle.
    display.fillarea(display.rows//2,display.cols//2,pink,animate,optimize)
    display.sleep(2,optimize)
