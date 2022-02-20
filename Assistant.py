#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging

# configure local dirs
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'fonts')

# add local packages to path
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in7b
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button
from signal import pause


# Print a message to the screen
# @params string
def printToDisplay(string):
    # Drawing on the Horizontal image. We must create an image object for both
    # the black layer and the red layer, even if we are only printing
    # to one layer
    # display size: 298*126
    HBlackImg = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)
    HRedImg = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)

    # create a draw object and the font object we will use for the display
    draw = ImageDraw.Draw(HBlackImg)
    font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    bangersFont = ImageFont.truetype(os.path.join(picdir, 'Bangers.ttc'), 18)

    # draw the text to the display. First argument is starting location
    # of the text in pixels
    draw.text((25, 65), string, font=font, fill=0)

    # Add the images to the display. Both the black and red layers need to
    # be passed in, even if we did not add anything to one of them
    epd.display(epd.getbuffer(HBlackImg), epd.getbuffer(HRedImg))
    # use line below to save to file instead
    # HBlackImg.save(fileName)


def handleBtnPress(btn):
    # get the button pin number
    pinNum = btn.pin.number

    # The number represents the pin number and
    # the value is the message we will print
    switcher = {
        5:  "Button 1",
        6:  "Button 2",
        13: "Button 3",
        19: "Button 4"
    }

    # get the string based on the passed in button and send it to printToDisplay()
    msg = switcher.get(pinNum, "Error")
    printToDisplay(msg)


try:
    # Map physical buttons to their GPIO pin
    btn1 = Button(5)
    btn2 = Button(6)
    btn3 = Button(13)
    btn4 = Button(19)

    # Init EPD and clear the screen
    epd = epd2in7b.EPD()  # get the display object and assing to epd
    epd.init()            # initialize the display
    epd.Clear()           # clear the display

    # Assign handlers to button press listeners
    btn1.when_pressed = handleBtnPress
    btn2.when_pressed = handleBtnPress
    btn3.when_pressed = handleBtnPress
    btn4.when_pressed = handleBtnPress
    pause()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in7b.epdconfig.module_exit()
    exit()
