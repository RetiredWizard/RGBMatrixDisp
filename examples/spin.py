from sys import stdin
from supervisor import runtime
import digitalio

import board
import rgbmatrix_coopmt
import math

try:
    addrPins = [
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC,
        board.MTX_ADDRD
    ]

    rgbPins=[
        board.MTX_R1,
    #    board.MTX_G1,
    #    board.MTX_B1,
        board.MTX_R2,
    #    board.MTX_G2,
    #    board.MTX_B2
    ]

    unused_rgbPins=[
    #    board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
    #    board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ]

    matrix = rgbmatrix_coopmt.RGBMatrix(32,64,0,addrPins,rgbPins,board.MTX_CLK,board.MTX_LAT,board.MTX_OE,unused_rgbPins)

# Teensy 4/4.1 pins
except:

    addrPins = [
        board.D21,
        board.D4,
        board.D20,
        board.D5,
        board.D3
    ]

    rgbPins=[
        board.D16,
        board.D1,
        board.D17,
        board.D23,
        board.D2,
        board.D22
    ]

    unused_rgbPins = None

    matrix = rgbmatrix_coopmt.RGBMatrix(64,64,0,addrPins,rgbPins,board.D19,board.D6,board.D18)

or1 = 0
oc1 = 0
or2 = 0
oc2 = 0

print("Press enter key to pause/restart...") 
rowcent = matrix.rows // 2
colcent = matrix.cols // 2
radius = min(matrix.rows, matrix.cols) // 3
color = 1

while True:
    for i in range(0,360,20):
        row1 = int(radius*math.cos(i*math.pi/180)) + rowcent
        col1 = int(radius*math.sin(i*math.pi/180)) + colcent
        row2 = int(radius*math.cos(((i+180)%360)*math.pi/180)) + rowcent
        col2 = int(radius*math.sin(((i+180)%360)*math.pi/180)) + colcent

        matrix.line(or1,oc1,or2,oc2,0)
        matrix.line(row1,col1,row2,col2,color)
        matrix.sleep(.05)
        if runtime.serial_bytes_available:
            matrix.input(None,True)
            while runtime.serial_bytes_available:
                stdin.read(1)
        or1 = row1
        oc1 = col1
        or2 = row2
        oc2 = col2
        
    color += 1
    if color >= 1 << (len(rgbPins)>>1):
        color = 1

matrix.input('test')

                
