#!/usr/bin/python
# -*- coding:utf-8 -*-

# *************************************************** 
#   This is a example program for
#   a Weather Station using Raspberry Pi B+, Waveshare ePaper Display and ProtoStax enclosure
#   --> https://www.waveshare.com/product/modules/oleds-lcds/e-paper/2.7inch-e-paper-hat-b.htm
#   --> https://www.protostax.com/products/protostax-for-raspberry-pi-b
#
#   This program is used to clear the ePaper display. If you are powering down your
#   Raspberry Pi and storing it and the ePaper display, it is recommended
#   that the display be cleared prior to storage, to prevent any burn-in.
 
#   Written by Sridhar Rajagopal for ProtoStax.
#   BSD license. All text above must be included in any redistribution
# *
import sys
sys.path.append(r'lib')

import epd2in13
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:
    epd = epd2in13.EPD()

    print("Clear...")
    epd.init()
    print("init EPD")
    epd.Clear()
    
    epd.sleep()
        
except :
    print ('traceback.format_exc():\n%s',traceback.format_exc())
    exit()
