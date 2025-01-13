from sys import stdin,implementation
import select
try:
    import digitalio
    import board
except:
    from machine import Pin
    
import math
try:
    import adafruit_ticks
except:
    import time as adafruit_ticks


class RGBMatrix:

    def __init__(self,rows,cols,brightness,addrPins,rgbPins,clockPin,latchPin,OEPin,unused_rgbPins=None):
        self.rows = rows
        self.cols = cols
        self.brightness = brightness
        self._framebuffer = []
        for i in range(self.rows):
            self._framebuffer.append(bytearray(self.cols))
        self._prevShiftReg1 = bytearray(self.cols)
        self._prevShiftReg2 = bytearray(self.cols)

        self._addrIO = []
        self._rgbIO = []
        self._unused_rgbIO = []

        if implementation.name.upper() == "MICROPYTHON":
            self._clockIO = Pin(clockPin,Pin.OUT)
            self._latchIO = Pin(latchPin,Pin.OUT)
            self._OEIO = Pin(OEPin,Pin.OUT)

            for pin in addrPins:
                self._addrIO.append(Pin(pin,Pin.OUT))
                self._addrIO[-1].value(False)

            for pin in rgbPins:
                self._rgbIO.append(Pin(pin,Pin.OUT))
                self._rgbIO[-1].value(False)

            if unused_rgbPins != None:
                for pin in unused_rgbPins:
                    self._unused_rgbIO.append(Pin(pin,Pin.OUT))
                    self._unused_rgbIO[-1].value(False)
        else:
            self._clockIO = digitalio.DigitalInOut(getattr(board,clockPin))
            self._clockIO.direction = digitalio.Direction.OUTPUT
            self._latchIO = digitalio.DigitalInOut(getattr(board,latchPin))
            self._latchIO.direction = digitalio.Direction.OUTPUT
            self._OEIO = digitalio.DigitalInOut(getattr(board,OEPin))
            self._OEIO.direction = digitalio.Direction.OUTPUT

            for pin in addrPins:
                self._addrIO.append(digitalio.DigitalInOut(getattr(board,pin)))
                self._addrIO[-1].direction = digitalio.Direction.OUTPUT
                self._addrIO[-1].value = False

            for pin in rgbPins:
                self._rgbIO.append(digitalio.DigitalInOut(getattr(board,pin)))
                self._rgbIO[-1].direction = digitalio.Direction.OUTPUT
                self._rgbIO[-1].value = False

            if unused_rgbPins != None:
                for pin in unused_rgbPins:
                    self._unused_rgbIO.append(digitalio.DigitalInOut(getattr(board,pin)))
                    self._unused_rgbIO[-1].direction = digitalio.Direction.OUTPUT
                    self._unused_rgbIO[-1].value = False

        self._numAddrPins = len(self._addrIO)
        self._numRGB = len(self._rgbIO) // 2
        self._updaterows = self.rows // 2

        for i in range(rows):
            self.sendrow(i)

    def _seconds(self):
        if hasattr(adafruit_ticks,'ticks_ms'):
            return adafruit_ticks.ticks_ms() / 1000
        else:
            return adafruit_ticks.monotonic_ns() / 1000000000

    def deinit(self):
        self.fill(0)

        del self._framebuffer
        del self._prevShiftReg1
        del self._prevShiftReg2

        if implementation.name.upper() == "CIRCUITPYTHON":
            self._clockIO.deinit()
            self._latchIO.deinit()
            self._OEIO.deinit()

            for pin in self._addrIO:
                pin.deinit()
            for pin in self._rgbIO:
                pin.deinit()
            for pin in self._unused_rgbIO:
                pin.deinit()
            
    def serial_bytes_available(self,timeout=1):
        # Does the same function as supervisor.runtime.serial_bytes_available
        spoll = select.poll()
        spoll.register(stdin,select.POLLIN)

        retval = spoll.poll(timeout)
        spoll.unregister(stdin)

        if not retval:
            retval = 0
        else:
            retval = 1

        return retval


    def fill(self,color):
        for i in range(self.rows):
            for j in range(self.cols):
                self._framebuffer[i][j] = color
            if color == 0:
                self.sendrow(i)

    def input(self,prompt=None,silent=False):

        while self.serial_bytes_available():
            stdin.read(1)

        if prompt != None:
            print(prompt,end="")

        keys = ""

        while keys[-1:] != '\n':
            self.refresh()
        
            if self.serial_bytes_available():
                try:
                    keys += stdin.read(1)
                    if keys[-1] in ['\x7f','\x08']:
                        keys = keys[:-2]
                        if not silent:
                            print('\x08'+'  \x08\x08',end="")
                    else:
                        if not silent:
                            print(keys[-1],end="")
                except:
                    pass

        return keys[:-1]

    def sleep(self,seconds,slow=False):
        timerEnd = self._seconds() + seconds
        if not slow:
            while self._seconds() < timerEnd:
                self.refresh()
        else:
            while self._seconds() < timerEnd:
                for row in range(self.rows):
                    self.sendrow(row)

    def off(self):
        if implementation.name.upper() == "CIRCUITPYTHON":
            self._OEIO.value = True     # display off
        else:
            self._OEIO.value(True)

    def refresh(self):
        adrline = []
        self._prevShiftReg1 = None
        for i in range(self._numAddrPins):   # set row to zero
            adrline.append(0)

        if implementation.name.upper() == "CIRCUITPYTHON":
            rowrange = 1 << self._numAddrPins
            for row in range(rowrange):
                row2 = row + rowrange

                # If row is different than previous
                if self._framebuffer[row] != self._prevShiftReg1 or \
                    self._framebuffer[row2] != self._prevShiftReg2:

                    self._prevShiftReg1 = self._framebuffer[row]   # save latched row
                    self._prevShiftReg2 = self._framebuffer[row2]

                    for col in range(self.cols):         # shift in row bits
                        for i in range(self._numRGB):
                            shft = 1 << ((self._numRGB-1) - i)
                            self._rgbIO[i].value = self._prevShiftReg1[col] & shft
                            self._rgbIO[i+self._numRGB].value = self._prevShiftReg2[col] & shft
    #                        self._rgbIO[i].value = self._framebuffer[row][col] & shft
    #                        self._rgbIO[i+self._numRGB].value = self._framebuffer[row2][col] & shft
                        self._clockIO.value = True
                        self._clockIO.value = False

                    self._OEIO.value = True                 # display off

                    self._latchIO.value = True       # latch new row
                    self._latchIO.value = False
                else:
                    if self.brightness > 0:              # brightness delay (hack)
                        timerEnd = self._seconds() + (self.brightness / 1000)
                        while self._seconds() < timerEnd:
                            pass

                for i in range(self._numAddrPins):      # move to new row
                    self._addrIO[i].value = adrline[i]

                self._OEIO.value = False             # display on

                # Binary increment of address lines
                adrline[0] = not adrline[0]
                for i in range(1,self._numAddrPins):
                    if not adrline[i-1]:
                        adrline[i] = not adrline[i]
                    else:
                        break

        else: # Micropython
            
            rowrange = 1 << self._numAddrPins
            for row in range(rowrange):
                row2 = row + rowrange

                # If row is different than previous
                if self._framebuffer[row] != self._prevShiftReg1 or \
                    self._framebuffer[row2] != self._prevShiftReg2:

                    self._prevShiftReg1 = self._framebuffer[row]   # save latched row
                    self._prevShiftReg2 = self._framebuffer[row2]

                    for col in range(self.cols):         # shift in row bits
                        for i in range(self._numRGB):
                            shft = 1 << ((self._numRGB-1) - i)
                            self._rgbIO[i].value(self._prevShiftReg1[col] & shft)
                            self._rgbIO[i+self._numRGB].value(self._prevShiftReg2[col] & shft)
                        self._clockIO.value(True)
                        self._clockIO.value(False)

                    self._OEIO.value(True)                 # display off

                    self._latchIO.value(True)       # latch new row
                    self._latchIO.value(False)
                else:
                    if self.brightness > 0:              # brightness delay (hack)
                        timerEnd = self._seconds() + (self.brightness / 1000)
                        while self._seconds() < timerEnd:
                            pass

                for i in range(self._numAddrPins):      # move to new row
                    self._addrIO[i].value(adrline[i])

                self._OEIO.value(False)             # display on

                # Binary increment of address lines
                adrline[0] = not adrline[0]
                for i in range(1,self._numAddrPins):
                    if not adrline[i-1]:
                        adrline[i] = not adrline[i]
                    else:
                        break
            

    def sendrow(self,row):

        if implementation.name.upper() == "CIRCUITPYTHON":
            self._OEIO.value = False

            if row < self._updaterows:
                row1 = row
                row2 = row + (self._updaterows)
            else:
                row1 = row - (self._updaterows)
                row2 = row

            self._prevShiftReg1 = self._framebuffer[row1]
            self._prevShiftReg2 = self._framebuffer[row2]
            for j in range(self.cols):
                for i in range(self._numRGB):
                    shft = 1 << ((self._numRGB-1) - i)
                    self._rgbIO[i].value = self._prevShiftReg1[j] & shft
                    self._rgbIO[i+self._numRGB].value = self._prevShiftReg2[j] & shft
                self._clockIO.value = True
                self._clockIO.value = False

            self._OEIO.value = True

            for i in range(self._numAddrPins):
                self._addrIO[i].value = (row) & (1<<i)

            self._latchIO.value = True
            self._latchIO.value = False

            self._OEIO.value = False
        else:     # Micropython
            self._OEIO.value(False)

            if row < self._updaterows:
                row1 = row
                row2 = row + (self._updaterows)
            else:
                row1 = row - (self._updaterows)
                row2 = row

            self._prevShiftReg1 = self._framebuffer[row1]
            self._prevShiftReg2 = self._framebuffer[row2]
            for j in range(self.cols):
                for i in range(self._numRGB):
                    shft = 1 << ((self._numRGB-1) - i)
                    self._rgbIO[i].value(self._prevShiftReg1[j] & shft)
                    self._rgbIO[i+self._numRGB].value(self._prevShiftReg2[j] & shft)
                self._clockIO.value(True)
                self._clockIO.value(False)

            self._OEIO.value(True)

            for i in range(self._numAddrPins):
                self._addrIO[i].value((row) & (1<<i))

            self._latchIO.value(True)
            self._latchIO.value(False)

            self._OEIO.value(False)

    def value(self,row,col):
        return self._framebuffer[row][col]

    def point(self,row,col,color=1):
        try:
            self._framebuffer[row][col] = color
        except:
            print(f'Bad row,col ({row},{col})')

    def _plotLineLow(self, x0, y0, x1, y1, color):
        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy

        D = (2 * dy) - dx
        y = y0

        for x in range(x0,x1+1):
            self.point(x, y, color)
            if D > 0:
                y = y + yi
                D = D + (2 * (dy - dx))
            else:
                D = D + 2*dy

    def _plotLineHigh(self, x0, y0, x1, y1, color):
        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        D = (2 * dx) - dy
        x = x0

        for y in range(y0,y1+1):
            self.point(x, y, color)
            if D > 0:
                x = x + xi
                D = D + (2 * (dx - dy))
            else:
                D = D + 2*dx

    def line(self, x0, y0, x1, y1, color=1):
        if abs(y1 - y0) < abs(x1 - x0):
            if x0 > x1:
                self._plotLineLow(x1, y1, x0, y0, color)
            else:
                self._plotLineLow(x0, y0, x1, y1, color)
        else:
            if y0 > y1:
                self._plotLineHigh(x1, y1, x0, y0, color)
            else:
                self._plotLineHigh(x0, y0, x1, y1, color)

    def _circleBres(self,centrow,centcol,row,col,color):
        self.point(centrow+row,centcol+col,color)
        self.point(centrow-row,centcol+col,color)
        self.point(centrow+row,centcol-col,color)
        self.point(centrow-row,centcol-col,color)
        self.point(centrow+col,centcol+row,color)
        self.point(centrow-col,centcol+row,color)
        self.point(centrow+col,centcol-row,color)
        self.point(centrow-col,centcol-row,color)

    def circle(self,centrow,centcol,radius,color=1):
        row = 0
        col = radius
        d = 3 - (2 * math.pi)
        self._circleBres(centrow,centcol,row,col,color)
        while col >= row:
            if d > 0:
                col -= 1
                d += 4*(row-col) + 10
            else:
                d += 4*row + 6

            row += 1

            self._circleBres(centrow,centcol,row,col,color)


    def dump(self):
        for i in range(self.rows):
            if i == 0:
                print('  ',end='')
                for k in range(self.cols):
                    print(k if k < 9 else 'X',end='')
                print()
            print(i if i < 9 else 'X',end=' ')
            for j in range(self.cols):
                print(self.value(i,j),end="")
            print()
