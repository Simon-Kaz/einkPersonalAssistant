#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging

# configure font dir
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')

# add local packages to path
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in7b
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button
from signal import pause

bFont = ImageFont.truetype(os.path.join(fontdir, 'Bangers.ttf'), 18)
regFont = ImageFont.truetype(os.path.join(fontdir, 'Font.ttc'), 18)


def mainScreen():
    # Create images, one for each layer - black and red
    HBlackImg = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)
    HRedImg = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)
    # Create draw objects
    drawblack = ImageDraw.Draw(HBlackImg)
    drawred = ImageDraw.Draw(HRedImg)
    # Add content to the images
    currentDateTime = datetime.now().strftime("%d/%m/%Y %H:%M")
    drawblack.text((15, 0), currentDateTime, font=bFont, fill=0)
    drawred.text((10, 20), 'TODO:', font=bFont, fill=0)
    drawblack.text((15, 60), 'get weather', font=bFont, fill=0)
    drawblack.text((15, 80), 'get tasks', font=bFont, fill=0)
    drawblack.text((15, 100), 'partial refresh', font=bFont, fill=0)
    # Render the images on the display
    # Both the black and red layers need to be passed in
    epd.display(epd.getbuffer(HBlackImg), epd.getbuffer(HRedImg))


def weatherDetailsScreen():
    HBlackImg = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)
    HRedImg = Image.new('1', (epd2in7b.EPD_HEIGHT, epd2in7b.EPD_WIDTH), 255)
    drawred = ImageDraw.Draw(HRedImg)
    # Add content to the images
    drawred.text((15, 0), "Weather Details", font=bFont, fill=0)
    epd.display(epd.getbuffer(HBlackImg), epd.getbuffer(HRedImg))


def handleBtnPress(btn):
    # get the button pin number
    pinNum = btn.pin.number

    # The number represents the pin number and
    # the value is the image we want to render
    switcher = {
        5:  mainScreen,
        6:  weatherDetailsScreen,
        13: weatherDetailsScreen,
        19: weatherDetailsScreen
    }

    # get the screen to render based on the passed in button
    renderScreen = switcher.get(pinNum, lambda: 'Invalid')
    renderScreen()


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
    # Continue running the app to allow for button press handling
    pause()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in7b.epdconfig.module_exit()
    exit()
