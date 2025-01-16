from sys import implementation
import rgbmatrix_coopmt

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
matrix = rgbmatrix_coopmt.RGBMatrix(rows,64,addrPins,rgbPins,clockPin,latchPin,OEPin,unused_rgbPins)

color = 1
ans = ''
while ans not in ['q','Q']:
    ans = ''
    while ans not in ['p','P','l','L','q','Q','s','S','c','C','f','F','a','A','g','G']:
        print('[f] fill/replace a color [a] fill an area [g] add polygon')
        ans = matrix.input('[p] add point, [l] add line, [s] set color, [c] add circle, [q] quit: ')
        if ans not in ['p','P','l','L','q','Q','s','s','c','C','f','F','a','A','g','G']:
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
        
        matrix.line(row1,col1,row2,col2,color)

    elif ans in ['g','G']:
        validentry = False
        ans = ''
        points = []
        while not validentry:
            for i in range(len(points)):
                print(points[i])

            print('\nEnter next row,col of polygon verticies')
            ans = matrix.input('(enter d when done, x to re-enter last point): ')

            if ans in ['d','D']:
                validentry = True
            elif ans in ['x','X']:
                points = points[:-1]
            else:
                try:
                    points.append([int(ans.split(',')[0]),int(ans.split(',')[1])])
                except:
                    print('Invalid Entry!')

        matrix.polygon(points,color)

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
    
    elif ans in ['f','F']:
        validentry = False
        ans = ''
        while not validentry:
            ans = matrix.input('Enter FillColor[,ReplaceColor=None[,Swap=False]]: ')
            try:
                anslist = ans.split(',')
                fillcolor = int(anslist[0])
                replacecolor = None
                swap = False
                if len(anslist) == 2:
                    replacecolor = int(anslist[1])
                elif len(anslist) == 3:
                    replacecolor = int(anslist[1])
                    if type(anslist[2]) == str:
                        swap =  anslist[2].upper() != 'FALSE'
                    else:
                        swap = int(anslist[2])
                else:
                    print('too many parameters')

                validentry = True
            except:
                print('Invalid Entry!')

            matrix.fill(fillcolor,replacecolor,swap)

    if ans in ['a','A']:
        validentry = False
        ans = ''
        while not validentry:
            ans = matrix.input('Enter row,col,color: ')
            try:
                r,c,clr = ans.split(',')
                row = int(r)
                col = int(c)
                color = int(clr)
                validentry = True
            except:
                print('Invalid Entry!')
        
        matrix.fillarea(row,col,color,True)
                    
    elif ans in ['q','Q']:
        matrix.deinit()
        