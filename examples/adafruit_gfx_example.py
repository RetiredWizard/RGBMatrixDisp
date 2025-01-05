# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test of primitive drawing with ILI9341 TFT display.
# This is made to work with ESP8266 MicroPython and the TFT FeatherWing, but
# adjust the SPI and display initialization at the start to change boards.
# Author: Tony DiCola
# License: MIT License (https://opensource.org/licenses/MIT)
import board
import rgbmatrix_coopmt
import adafruit_gfx.gfx

try:
    addrPins = [board.MTX_ADDRA,board.MTX_ADDRB,board.MTX_ADDRC,board.MTX_ADDRD]

#    rgbPins=[board.MTX_R1,board.MTX_G1,board.MTX_B1,board.MTX_R2,board.MTX_G2,board.MTX_B2]
#    unused_rgbPins = None
    # for Single color (red), allows for faster refresh on slower boards
    rgbPins=[board.MTX_R1,board.MTX_R2,]
    # defining unused pins allows library to ensure noise doesn't show up as color data
    unused_rgbPins=[board.MTX_G1,board.MTX_B1,board.MTX_G2,board.MTX_B2]

    display = rgbmatrix_coopmt.RGBMatrix(32,64,0,addrPins,rgbPins,board.MTX_CLK,board.MTX_LAT,board.MTX_OE,unused_rgbPins)

# Teensy 4/4.1 pins
except:

    addrPins = [board.D21,board.D4,board.D20,board.D5,board.D3]
    rgbPins=[board.D16,board.D1,board.D17,board.D23,board.D2,board.D22]
    display = rgbmatrix_coopmt.RGBMatrix(64,64,0,addrPins,rgbPins,board.D19,board.D6,board.D18)

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