A pure Python library for driving HUB75 type RGB Matrix panels. The goal is to provide graphics functions that will run on CircuitPython or MicroPython for boards that don't have firmware support for RGB Matrix panels, like the mimxrt10xx (teensy 4/4.1) or broadcom (RPi Zero 2w) boards. As demonstrated in the provided examples this library works well with the [Adafruit_CircuitPython_GFX](https://github.com/adafruit/Adafruit_CircuitPython_GFX) libaray for both CircuitPython and MicroPython   


class **rgbmatrix_coopmt.RGBMatrix**(*, **rows**:*int*, **cols**:*int*, **addrPins**:*list[str]*, **rgbPins**:*list[str]*, **clockPin**:*str*, **latchPin**:*str*, **OEPin**:*str*, **unused_rgbPins**:*list[str]*=None)   

A driver for HUB75 RGB matrix display panels.   

The RGBMatrix.refresh() method must be called as frequently as possible to maintain the
displayed image. To help facilitate the continual refresh of the matrix this library provides
an RGBMatrix.sleep() method which will refresh the display while sleeping and an
RGBMatrix.input() method which will refresh the display while waiting for user input.   

.. param *int* **rows**: The number of rows in the RGB matrix.   

.. param *int* **cols**: The number of columns in the RGB matrix.   

.. param *list[str]* **addrPins**: String representations of the matrix's address pins in the order
    (A, B, C, D, ...). For CircuitPython the strings should be BOARD attributes and for 
    MicroPython the strings should be valid machine.Pin parameters.   

.. param *list[str]* **rgbPins**: String representations of the matrix's RGB pins in the order
    (R1, G1, B1, R2, G2, B2). For CircuitPython the strings should be BOARD attributes and for MicroPython the strings should be valid machine.Pin parameters. Typically on HUB75 RGB matricies "color depth" and pixel brightness is controlled by varying the amount of time (PWM) an LED is on during a refresh cycle, however due to the speed limitations of this implementation each Red, Green or Blue LED is either on or off each refresh cycle so while 8 colors can be displayed there is no additional depth or brightness control available.   

.. param *str* **clockPin**: String representations of the matrix's clock pin. For CircuitPython the
    string should be a BOARD attribute and for MicroPython the string should be valid machine.Pin parameter.   

.. param *str* **latchPin**: String representations of the matrix's latch pin. For CircuitPython the
    string should be a BOARD attribute and for MicroPython the string should be valid machine.Pin parameter.   

.. param *str* **OEPin**: String representations of the matrix's output enable pin. For CircuitPython the
    string should be a BOARD attribute and for MicroPython the string should be valid machine.Pin parameter.   

.. param *list[str]* **unused_rgbPins**: String representations of the matrix's unused address pins in the order
    (R1, G1, B1, R2, G2, B2). Select colors may be excluded from processing in order to improve
    update speed and reduce flickering. Any pins linsted in the parameter should be omitted from the 
    rgbPins parameter. For CircuitPython the strings should be BOARD attributes and for MicroPython the
    strings should be valid machine.Pin parameters.   

.. py:method:: RGBMatrix.**deinit()**   

    Attempts to free up used memory and release locked resources (CircuitPython Pins)   

.. py:method:: RGBMatrix.**serial_bytes_available(timeout=1)**   

    Performs a non-blocking check to see if any UART input is available for processing   

.. py:method:: RGBMatrix.**fill(color,replace=None,swap=False)**   

    Colors all pixels the supplied "color". The color value can be 0-7. If a color value is passed
    as the replace argument then only pixels that are currently the "replace" color will be
    replaced (filled) with the new "color" value. The swap parameter modifies the replace function
    by also replacing (filling) any existing pixels that were originally the "replace" color with
    "color" pixels, essentially swapping the "color" and "replace" colored pixels.   

.. py:method:: RGBMatrix.**fillarea(row,col,color,animate=False,optimize=True)**

    Colors all pixels within a bounded area the supplied "color". The color value can be 0-7. The
    background color being replaced is whatever color is at location (row,col). Any pixels which
    are the background color are replaced until a pixel of a different color or the display border
    is encountered. Filling proceeds outward from the (row,col) point. If animate is to True the screen will be refreshed as the fill occurs. The optimize parameter is used during the fill
    animation if enabled.   

.. py:method:: RGBMatrix.**input(prompt=None,optimize=True,silent=False)**   

    Displays a prompt if provided and waits for user input. While waiting the RGB matrix display 
    is refreshed using the specified optimize value (see RGBMatrix.refresh). If the slient 
    parameter is set to True, the users input is not echoed/displayed.   

.. py:method:: RGBMatrix.**sleep(seconds,optimize=True)**   

    sleeps for a given number of seconds. While sleeping the RGB matrix display is refreshed using 
    the specified optimize value (see RGBMatrix.refresh).   

.. py:method:: RGBMatrix.**off()**   

    Turns the display off.   

.. py:method:: RGBMatrix.**refresh(optimize=True)**   

    Refreshes the RGB matrix display. This function must be performed as frequently as possible. 
    If the optimize parameter is left as True, any row that has the same framebuffer values as 
    the previously displayed row will be be displayed without shifting the color values from the 
    framebuffer. With some display patterns this can signficantly increase the refresh speed, 
    however it can also result in an uneven brightness of rows since some rows spend more time 
    being displayed while the shift registers are being filled. Setting optimize to False 
    disables this optimization.

.. py:method:: RGBMatrix.**sendrow(row)**   

    Refreshes a single row of the display.   

.. py:method:: RGBMatrix.**value(row,col)**   

    Returns the color value currently being display at the (row,col) point.   

.. py:method:: RGBMatrix.**point(row,col,color)**   

    Sets the color value to be displayed at the (row,col) point. The color value can be 0-7.    

.. py:method:: RGBMatrix.**line(row0, col0, row1, col1, color=1)**   

    Draws a straight line of color (0-7) between points (row0,col0) and (row1,col1). There is likely 
    no performance advanage to using this method over the adafruit_gfx.gfx line method. To use 
    the adafruit_gfx library with Micropython the Python source version should be downloaded from 
    github (https://github.com/adafruit/Adafruit_CircuitPython_GFX)   

.. py:method:: RGBMatrix.**polygon(points, color=1)**

    The points argument is a list of points that make up a polygon. Each point is a list consisting
    of a row,col pair. The method will draw a straight line betweeen each of the points and then a
    final straight line between the last point and the first point, closing the polygon.   

.. py:method:: RGBMatrix.**circle(centrow,centcol,radius,color=1)**   

    Draws a circle of radius and color (0-7) centered at points (centrow,centcol). There is likely 
    no performance advanage to using this method over the adafruit_gfx.gfx circle method. To use 
    the adafruit_gfx library with Micropython the Python source version should be downloaded from 
    github (https://github.com/adafruit/Adafruit_CircuitPython_GFX)   

.. py:method:: RGBMatrix.**dump()**   

    Prints a matrix to the serial terminal representing the RGB matrix framebuffer.   

