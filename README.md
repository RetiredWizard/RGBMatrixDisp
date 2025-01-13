A pure Python library for driving HUB75 type RGB Matrix panels. The goal is to provide graphics functions that will run on CircuitPython or MicroPython for boards that don't have firmware support for RGB Matrix panels. As demonstrated in the provided examples this library works well with the [Adafruit_CircuitPython_GFX](https://github.com/adafruit/Adafruit_CircuitPython_GFX) libaray for both CircuitPython and MicroPython   


    class gbmatrix_coopmt.RGBMatrix(*,rows:int,cols:int,brightness:float,addrPins:list[str],rgbPins:list[str],clockPin:str,latchPin:str,OEPin:str,unused_rgbPins:list[str]=None)

    A driver for HUB75 RGB matrix display panels.

    The RGBMatrix.refresh() method must be called as frequently as possible to maintain the
    displayed image. To help faciliate the continual refresh of the matrix this library provides
    an RGBMatrix.sleep() method which will refresh the display while sleeping and an
    RGBMatrix.input() method which will refresh the display while waiting for user input.   

    :param int rows: The number of rows in the RGB matrix.   
    :param int cols: The number of columns in the RGB matrix.   
    :param float brightness: A brightness modification for tweaking the uneven brightness resulting
        from differing row timings due to speed optimizations. (a value of 0 disables the feature)   
    :param list[str] addrPins: String representations of the matrix's address pins in the order
        (A, B, C, D, ...). For CircuitPython the strings should be BOARD attributes and for 
        MicroPython the strings should be valid machine.Pin parameters.   
    :param list[str] rgbPins: String representations of the matrix's address pins in the order
        (R1, G1, B1, R2, G2, B2). For CircuitPython the strings should be BOARD attributes and for 
        MicroPython the strings should be valid machine.Pin parameters.   
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

    .. py:method:: RGBMatrix.fill(color)   

        Colors all pixels the given ***color***.   

    .. py:method:: RGBMatrix.input(prompt=None,silent=False)   

        Displays a prompt if provided and waits for user input. While waiting the RGB matrix display is
        refreshed. If the slient parameter is set to True, the users input is not echo/displayed.   

    .. py:method:: RGBMatrix.sleep(seconds,slow=False)   

        sleeps for a given number of seconds. While sleeping the RGB matrix display is refreshed.
        If the slow parameter is set to True, display speed optimizations will be turned off resulting
        in more flicker but a more uniform display brigtness across rows.   

    .. py:method:: RGBMatrix.off()   

        Turns the display off.   

    .. py:method:: RGBMatrix.refresh()   

        Refreshes the RGB matrix display. This function must be performed a frequently as possible.   

    .. py:method:: RGBMatrix.sendrow(row)   

        Refreshes a single row of the display.   

    .. py:method:: RGBMatrix.value(row,col)   

        Returns the color value currently being display at the (row,col) point.   

    .. py:method:: RGBMatrix.point(row,col,color)   

        Sets the color value to be displayed at the (row,col) point.   

    .. py:method:: RGBMatrix.line(row0, col0, row1, col1, color=1)   

        Draws a straight line of color between points (row0,col0) and (row1,col1). There is likely no 
        performance advanage of using this method over the adafruit_gfx.gfx line method. To use the
        adafruit_gfx library with Micropython the Python source version should be downloaded from 
        github (https://github.com/adafruit/Adafruit_CircuitPython_GFX)   

    .. py:method:: RGBMatrix.circle(centrow,centcol,radius,color=1)   

        Draws a circle of radius and color centered at points (centrow,centcol). There is likely no 
        performance advanage of using this method over the adafruit_gfx.gfx circle method. To use the
        adafruit_gfx library with Micropython the Python source version should be downloaded from 
        github (https://github.com/adafruit/Adafruit_CircuitPython_GFX)   

    .. py:method:: RGBMatrix.dump()   

        Prints a matrix to the serial terminal representing the RGB matrix framebuffer.   

