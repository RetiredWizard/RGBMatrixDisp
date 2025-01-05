import board
import rgbmatrix_coopmt

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

lines = []
points = []
color = 1

ans = ''
while ans not in ['q','Q']:
    if len(lines) > 0:
        print('Lines:')
        for i in range(len(lines)):
            print(lines[i])
    if len(points) > 0:
        print('Points:')
        for i in range(len(points)):
            print(points[i])

    ans = ''
    while ans not in ['p','P','l','L','q','Q','s','S','c','C']:
        ans = matrix.input('[p] add point, [l] add line, [s] set color, [c] add circle, [q] quit: ')
        if ans not in ['p','P','l','L','q','Q','s','s','c','C']:
            print('Invalid Entry!')

    if ans in ['p','P']:
        validentry = False
        ans = ''
        while not validentry:
            ans = matrix.input('Enter row,col: ')
            try:
                r,c = ans.split(',')
                row = int(r)
                col = int(c)
                validentry = True
            except:
                print('Invalid Entry!')
        
        points.append((row,col))
        matrix.point(row,col,color)
        
    elif ans in ['l','L']:
        validentry = False
        ans = ''
        while not validentry:
            ans = matrix.input('Enter row1,col1,row2,col2: ')
            try:
                r1,c1,r2,c2 = ans.split(',')
                row1 = int(r1)
                col1 = int(c1)
                row2 = int(r2)
                col2 = int(c2)
                validentry = True
            except:
                print('Invalid Entry!')
        
        lines.append(((row1,col1),(row2,col2)))
        matrix.line(row1,col1,row2,col2,color)

    elif ans in ['s','S']:
        color = int(matrix.input(f'[{color}] Enter new color value: '))
        
    elif ans in ['c','C']:
        validentry = False
        ans = ''
        while not validentry:
            ans = matrix.input('Enter RowCent,ColCent,radius: ')
            try:
                r1,c1,rad = ans.split(',')
                row = int(r1)
                col = int(c1)
                radius = int(rad)
                validentry = True
            except:
                print('Invalid Entry!')

            matrix.circle(row,col,radius,color)
            
    elif ans in ['q','Q']:
        matrix.deinit()
        