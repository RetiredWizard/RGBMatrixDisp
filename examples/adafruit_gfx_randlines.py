# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Random line drawing with ILI9341 TFT display.
# This is made to work with ESP8266 MicroPython and the TFT FeatherWing, but
# adjust the SPI and display initialization at the start to change boards.
# Author: Tony DiCola
# License: MIT License (https://opensource.org/licenses/MIT)
import board
import rgbmatrix_coopmt
import adafruit_gfx.gfx

try:
    from random import randrange
except:
    import os
    def randrange(min_value, max_value):
        # Simple randrange implementation for ESP8266 uos.urandom function.
        # Returns a random integer in the range min to max.  Supports only 32-bit
        # int values at most.
        magnitude = abs(max_value - min_value)
        randbytes = os.urandom(4)
        offset = int(
            (randbytes[3] << 24) | (randbytes[2] << 16) | (randbytes[1] << 8) | randbytes[0]
        )
        offset %= magnitude + 1  # Offset by one to allow max_value to be included.
        return min_value + offset

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