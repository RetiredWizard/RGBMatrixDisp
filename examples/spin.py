from sys import stdin,implementation
import rgbmatrix_coopmt
import math

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
    addrPins = ["D21","D4","D20","D5","D3"]
    rgbPins=["D16","D1","D17","D23","D2","D22"]
    clockPin = "D19"
    latchPin = "D6"
    OEPin ="D18"
    unused_rgbPins = None

rows = 2 ** (len(addrPins)+1)
matrix = rgbmatrix_coopmt.RGBMatrix(rows,64,0,addrPins,rgbPins,clockPin,latchPin,OEPin,unused_rgbPins)

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
        if matrix.serial_bytes_available():
            matrix.input(None,True)
            while matrix.serial_bytes_available():
                stdin.read(1)
        or1 = row1
        oc1 = col1
        or2 = row2
        oc2 = col2
        
    color += 1
    if color >= 1 << (len(rgbPins)>>1):
        color = 1

matrix.input('test')

                
