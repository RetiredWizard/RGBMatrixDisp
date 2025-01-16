"""
`rgbmatrix` - Hub75 RGB Matrix driver
====================================================

* Author(s): RetiredWizard

"""

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

__version__ = "0.1.0+auto.0"
__repo__ = "https://github.com/retiredwizard/RGBMatrixDisp.git"

class RGBMatrix:
    """
    A driver for HUB75 RGB matrix display panels.

    The RGBMatrix.refresh() method must be called as frequently as possible to maintain the
    displayed image. To help facilitate the continual refresh of the matrix this library provides
    an RGBMatrix.sleep() method which will refresh the display while sleeping and an
    RGBMatrix.input() method which will refresh the display while waiting for user input.

    :param int rows: The number of rows in the RGB matrix.
    :param int cols: The number of columns in the RGB matrix.
    :param list[str] addrPins: String representations of the matrix's address pins in the order
        (A, B, C, D, ...). For CircuitPython the strings should be BOARD attributes and for 
        MicroPython the strings should be valid machine.Pin parameters.
    :param list[str] rgbPins: String representations of the matrix's RGB pins in the order
        (R1, G1, B1, R2, G2, B2). For CircuitPython the strings should be BOARD attributes and for 
        MicroPython the strings should be valid machine.Pin parameters. Typically on HUB75 RGB
        matricies "color depth" and pixel brightness is controlled by varying the amount of time (PWM)
        an LED is on during a refresh cycle, however due to the speed limitations of this implementation
        each Red, Green or Blue LED is either on or off each refresh cycle so while 8 colors can be
        displayed there is no additional depth or brightness control available.   
    :param str clockPin: String representations of the matrix's clock pin. For CircuitPython the
        string should be a BOARD attribute and for MicroPython the string should be valid machine.Pin parameter.
    :param str latchPin: String representations of the matrix's latch pin. For CircuitPython the
        string should be a BOARD attribute and for MicroPython the string should be valid machine.Pin parameter.
    :param str OEPin: String representations of the matrix's output enable pin. For CircuitPython the
        string should be a BOARD attribute and for MicroPython the string should be valid machine.Pin parameter.
    :param list[str] unused_rgbPins: String representations of the matrix's unused address pins in the order
        (R1, G1, B1, R2, G2, B2). Select colors may be excluded from processing in order to improve
        update speed and reduce flickering. Any pins linsted in the parameter should be omitted from the 
        rgbPins parameter. For CircuitPython the strings should be BOARD attributes and for MicroPython the
        strings should be valid machine.Pin parameters.
    
    .. py:method:: RGBMatrix.deinit()

        Attempts to free up used memory and release locked resources (CircuitPython Pins)

    .. py:method:: RGBMatrix.serial_bytes_available(timeout=1)

        Performs a non-blocking check to see if any uart input is available for processing

    .. py:method:: RGBMatrix.fill(color,replace=None,swap=False)

        Colors all pixels the supplied "color". The color value can be 0-7. If a color value is passed
        as the replace argument then only pixels that are currently the "replace" color will be
        replaced (filled) with the new "color" value. The swap parameter modifies the replace function
        by also replacing (filling) any existing pixels that were originally the "replace" color with
        "color" pixels, essentially swapping the "color" and "replace" colored pixels.

    .. py:method:: RGBMatrix.fillarea(row,col,color)

        Colors all pixels within a bounded area the supplied "color". The color value can be 0-7. The
        background color being replaced is whatever color is at location (row,col). Any pixels which are the
        background color are replaced until a pixel of a different color or the display border is
        encountered. Filling proceeds outward from the (row,col) point.

    .. py:method:: RGBMatrix.input(prompt=None,optimize=True,silent=False)

        Displays a prompt if provided and waits for user input. While waiting the RGB matrix display is   
        refreshed using the specified optimize value (see RGBMatrix.refresh). If the slient parameter   
        is set to True, the user's input is not echoed/displayed.   

    .. py:method:: RGBMatrix.sleep(seconds,optimize=True)

        sleeps for a given number of seconds. While sleeping the RGB matrix display is refreshed using   
        the specified optimize value (see RGBMatrix.refresh).   

    .. py:method:: RGBMatrix.off()

        Turns the display off.

    .. py:method:: RGBMatrix.refresh(optimize=True)

        Refreshes the RGB matrix display. This function must be performed as frequently as possible.
        If the optimize parameter is left as True, any row that has the same framebuffer values as the
        previously displayed row will be be displayed without shifting the color values from the
        framebuffer. With some display patterns this can signficantly increase the refresh speed,
        however it can also result in an uneven brightness of rows since some rows spend more time
        being displayed while the shift registers are being filled. Setting optimize to False disables
        this optimization.

    .. py:method:: RGBMatrix.sendrow(row)

        Refreshes a single row of the display.

    .. py:method:: RGBMatrix.value(row,col)

        Returns the color value currently being display at the (row,col) point.

    .. py:method:: RGBMatrix.point(row,col,color)

        Sets the color value to be displayed at the (row,col) point. The color value can be 0-7.

    .. py:method:: RGBMatrix.line(row0, col0, row1, col1, color=1)

        Draws a straight line of color (0-7) between points (row0,col0) and (row1,col1). There is likely no 
        performance advanage of using this method over the adafruit_gfx.gfx line method. To use the
        adafruit_gfx library with Micropython the Python source version should be downloaded from 
        github (https://github.com/adafruit/Adafruit_CircuitPython_GFX)

    .. py:method:: RGBMatrix.polygon(points, color=1)

        The points argument is a list of points that make up a polygon. Each point is a list consisting of 
        a row,col pair. The method will draw a straight line betweeen each of the points and then a final
        straight line between the last point and the first point, closing the polygon.

    .. py:method:: RGBMatrix.circle(centrow,centcol,radius,color=1)

        Draws a circle of radius and color (0-7) centered at points (centrow,centcol). There is likely no 
        performance advanage of using this method over the adafruit_gfx.gfx circle method. To use the
        adafruit_gfx library with Micropython the Python source version should be downloaded from 
        github (https://github.com/adafruit/Adafruit_CircuitPython_GFX)

    .. py:method:: RGBMatrix.dump()

        Prints a matrix to the serial terminal representing the RGB matrix framebuffer.

    """

    def __init__(self,rows,cols,addrPins,rgbPins,clockPin,latchPin,OEPin,unused_rgbPins=None):

        if rows != 2 ** (len(addrPins)+1):
            raise ValueError(f'A matrix with {rows} rows requires {len(bin(rows))-4} Address Pins')

        self.rows = rows
        self.cols = cols
        self._framebuffer = []
        for i in range(self.rows):
            self._framebuffer.append(bytearray(self.cols))
        self._prevShiftReg1 = None
        self._prevShiftReg2 = None

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
        self._adrline = [0] * self._numAddrPins
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


    def fill(self,color,replace=None,swap=False):
        for i in range(self.rows):
            for j in range(self.cols):
                if replace is None or self._framebuffer[i][j] == replace:
                    self._framebuffer[i][j] = color
                elif replace is not None and swap and self._framebuffer[i][j] == color:
                    self._framebuffer[i][j] = replace
            if color == 0 and replace is None:
                self.sendrow(i)

    def fillarea(self,row,col,color=1):
        if self._framebuffer[row][col] != color:
            blankcolor = self._framebuffer[row][col]
            self._framebuffer[row][col] = 255
            done = False
            while not done:
                done = True
                for i in range(self.rows):
                    for j in range(self.cols):
                        if self._framebuffer[i][j] == 255:
                            if self._framebuffer[max(0,i-1)][j] == blankcolor:
                                self._framebuffer[max(0,i-1)][j] = 255
                                done = False
                            if self._framebuffer[min(self.rows-1,i+1)][j] == blankcolor:
                                self._framebuffer[min(self.rows-1,i+1)][j] = 255
                                done = False
                            if self._framebuffer[i][max(0,j-1)] == blankcolor:
                                self._framebuffer[i][max(0,j-1)] = 255
                                done = False
                            if self._framebuffer[i][min(self.cols-1,j+1)] == blankcolor:
                                self._framebuffer[i][min(self.cols-1,j+1)] = 255
                                done = False
                self.refresh(optimize=False)
            self.fill(color,255)

    def input(self,prompt=None,optimize=True,silent=False):

        while self.serial_bytes_available():
            stdin.read(1)

        if prompt != None:
            print(prompt,end="")

        keys = ""

        while keys[-1:] != '\n':
            self.refresh(optimize)
        
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

    def sleep(self,seconds,optimize=True):
        timerEnd = self._seconds() + seconds
        while self._seconds() < timerEnd:
            self.refresh(optimize)

    def off(self):
        if implementation.name.upper() == "CIRCUITPYTHON":
            self._OEIO.value = True     # display off
        else:
            self._OEIO.value(True)

    def refresh(self,optimize=True):
        rowrange = 1 << self._numAddrPins
        if implementation.name.upper() == "CIRCUITPYTHON":
            for row in range(rowrange):
                row2 = row + rowrange

                # If row is different than previous
                if not optimize or self._framebuffer[row] != self._prevShiftReg1 or \
                    self._framebuffer[row2] != self._prevShiftReg2:

                    self._prevShiftReg1 = self._framebuffer[row]   # save latched row
                    self._prevShiftReg2 = self._framebuffer[row2]

                    for col in range(self.cols):         # shift in row bits
                        shft = 1 << (self._numRGB-1)
                        self._rgbIO[0].value = self._prevShiftReg1[col] & shft
                        self._rgbIO[self._numRGB].value = self._prevShiftReg2[col] & shft
                        if shft > 1:
                            shft >>= 1
                            self._rgbIO[1].value = self._prevShiftReg1[col] & shft
                            self._rgbIO[1+self._numRGB].value = self._prevShiftReg2[col] & shft
                            if shft > 1:
                                shft = 1
                                self._rgbIO[2].value = self._prevShiftReg1[col] & shft
                                self._rgbIO[2+self._numRGB].value = self._prevShiftReg2[col] & shft
                        self._clockIO.value = True
                        self._clockIO.value = False

                self._OEIO.value = True                 # display off

                self._latchIO.value = True       # latch new row
                self._latchIO.value = False

                for i in range(self._numAddrPins):      # move to new row
                    self._addrIO[i].value = self._adrline[i]

                self._OEIO.value = False             # display on

                # Binary increment of address lines
                self._adrline[0] = not self._adrline[0]
                for i in range(1,self._numAddrPins):
                    if not self._adrline[i-1]:
                        self._adrline[i] = not self._adrline[i]
                    else:
                        break

        else: # Micropython
            
            for row in range(rowrange):
                row2 = row + rowrange

                # If row is different than previous
                if optimize and (self._framebuffer[row] != self._prevShiftReg1 or \
                    self._framebuffer[row2] != self._prevShiftReg2):

                    self._prevShiftReg1 = self._framebuffer[row]   # save latched row
                    self._prevShiftReg2 = self._framebuffer[row2]

                    for col in range(self.cols):         # shift in row bits
                        shft = 1 << (self._numRGB-1)
                        self._rgbIO[0].value(self._prevShiftReg1[col] & shft)
                        self._rgbIO[self._numRGB].value(self._prevShiftReg2[col] & shft)
                        if shft > 1:
                            shft >>= 1
                            self._rgbIO[1].value(self._prevShiftReg1[col] & shft)
                            self._rgbIO[1+self._numRGB].value(self._prevShiftReg2[col] & shft)
                            if shft > 1:
                                shft = 1
                                self._rgbIO[2].value(self._prevShiftReg1[col] & shft)
                                self._rgbIO[2+self._numRGB].value(self._prevShiftReg2[col] & shft)
                        self._clockIO.value(True)
                        self._clockIO.value(False)

                self._OEIO.value(True)                 # display off

                self._latchIO.value(True)       # latch new row
                self._latchIO.value(False)

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
                shft = 1 << (self._numRGB-1)
                self._rgbIO[0].value = self._prevShiftReg1[j] & shft
                self._rgbIO[self._numRGB].value = self._prevShiftReg2[j] & shft
                if shft > 1:
                    shft >>= 1
                    self._rgbIO[1].value = self._prevShiftReg1[j] & shft
                    self._rgbIO[1+self._numRGB].value = self._prevShiftReg2[j] & shft
                    if shft > 1:
                        shft = 1
                        self._rgbIO[2].value = self._prevShiftReg1[j] & shft
                        self._rgbIO[2+self._numRGB].value = self._prevShiftReg2[j] & shft
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
                shft = 1 << (self._numRGB-1)
                self._rgbIO[0].value(self._prevShiftReg1[j] & shft)
                self._rgbIO[self._numRGB].value(self._prevShiftReg2[j] & shft)
                if shft > 1:
                    shft >>= 1
                    self._rgbIO[1].value(self._prevShiftReg1[j] & shft)
                    self._rgbIO[1+self._numRGB].value(self._prevShiftReg2[j] & shft)
                    if shft > 1:
                        shft = 1
                        self._rgbIO[2].value(self._prevShiftReg1[j] & shft)
                        self._rgbIO[2+self._numRGB].value(self._prevShiftReg2[j] & shft)
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

    def polygon(self,points,color=1):
        if len(points) > 1:
            for i in range(1,len(points)):
                self.line(points[i-1][0],points[i-1][1],points[i][0],points[i][1],color)

            self.line(points[-1][0],points[-1][1],points[0][0],points[0][1],color)

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
