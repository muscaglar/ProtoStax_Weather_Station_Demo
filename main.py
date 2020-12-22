#!/usr/bin/python
# -*- coding:utf-8 -*-

# *************************************************** 
#   This is a example program for
#   a Weather Station using Raspberry Pi B+, Waveshare ePaper Display and ProtoStax enclosure
#   --> https://www.waveshare.com/product/modules/oleds-lcds/e-paper/2.7inch-e-paper-hat-b.htm
#   --> https://www.protostax.com/products/protostax-for-raspberry-pi-b
#
#   It uses the weather API provided by Open Weather Map (https://openweathermap.org/api) to
#   query the current weather for a given location and then display it on the ePaper display.
#   It refreshes the weather information every 10 minutes and updates the display.

#   Written by Sridhar Rajagopal for ProtoStax.
#   BSD license. All text above must be included in any redistribution
# *
import sys

sys.path.append(r'lib')

import signal
import epd2in13
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

import pyowm

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

owm = pyowm.OWM('a5070083604b9887f1f3a47884181686')

city_id = 2643743  # London

weather_icon_dict = {200: "6", 201: "6", 202: "6", 210: "6", 211: "6", 212: "6",
                     221: "6", 230: "6", 231: "6", 232: "6",

                     300: "7", 301: "7", 302: "8", 310: "7", 311: "8", 312: "8",
                     313: "8", 314: "8", 321: "8",

                     500: "7", 501: "7", 502: "8", 503: "8", 504: "8", 511: "8",
                     520: "7", 521: "7", 522: "8", 531: "8",

                     600: "V", 601: "V", 602: "W", 611: "X", 612: "X", 613: "X",
                     615: "V", 616: "V", 620: "V", 621: "W", 622: "W",

                     701: "M", 711: "M", 721: "M", 731: "M", 741: "M", 751: "M",
                     761: "M", 762: "M", 771: "M", 781: "M",

                     800: "1",

                     801: "H", 802: "N", 803: "N", 804: "Y"
                     }


# Main function

def main():
    print("hello")
    epd = epd2in13.EPD()
    print("got EPD")
    while True:

        obs = owm.weather_at_id(city_id)
        location = obs.get_location().get_name()
        weather = obs.get_weather()
        reftime = weather.get_reference_time()
        description = weather.get_detailed_status()
        temperature = weather.get_temperature(unit='celsius')
        humidity = weather.get_humidity()
        pressure = weather.get_pressure()
        clouds = weather.get_clouds()
        wind = weather.get_wind()
        rain = weather.get_rain()
        sunrise = weather.get_sunrise_time()
        sunset = weather.get_sunset_time()

        print("location: " + location)
        print("weather: " + str(weather))
        print("description: " + description)
        print("temperature: " + str(temperature))
        print("humidity: " + str(humidity))
        print("pressure: " + str(pressure))
        print("clouds: " + str(clouds))
        print("wind: " + str(wind))
        print("rain: " + str(rain))
        print("sunrise: " + time.strftime('%H:%M', time.localtime(sunrise)))
        print("sunset: " + time.strftime('%H:%M', time.localtime(sunset)))

        # Display Weather Information on e-Paper Display
        try:
            print("Clear...")
            epd.init()
            print("init EPD")
            epd.Clear()

            # Drawing on the Horizontal image
            HBlackimage = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255)  # 298*126
            HRedimage = Image.new('1', (epd2in13.EPD_HEIGHT, epd2in13.EPD_WIDTH), 255)  # 298*126

            print("Drawing")
            drawblack = ImageDraw.Draw(HBlackimage)
            drawred = ImageDraw.Draw(HRedimage)

            font24 = ImageFont.truetype('fonts/arial.ttf', 20)
            font16 = ImageFont.truetype('fonts/arial.ttf', 12)
            font20 = ImageFont.truetype('fonts/arial.ttf', 16)
            fontweather = ImageFont.truetype('fonts/meteocons-webfont.ttf', 24)
            fontweather_small = ImageFont.truetype('fonts/meteocons-webfont.ttf', 20)
            fontweatherbig = ImageFont.truetype('fonts/meteocons-webfont.ttf', 52)

            w1, h1 = font24.getsize(location)
            w2, h2 = font20.getsize(description)
            w3, h3 = fontweatherbig.getsize(weather_icon_dict[weather.get_weather_code()])

            drawblack.text((5, 5), "Juan's London", font=font24, fill=0)
            drawblack.text((50 + (w1 / 2 - w2 / 2), 25), description, font=font20, fill=0)
            drawred.text((210 - w3 - 10, 0), weather_icon_dict[weather.get_weather_code()], font=fontweatherbig, fill=0)
            drawblack.text((5, 42), "Observed at: " + time.strftime('%I:%M %p', time.localtime(reftime)), font=font16,
                           fill=0)

            tempstr = str("{0}{1}C".format(int(round(temperature['temp'])), u'\u00b0'))
            print(tempstr)
            w4, h4 = font24.getsize(tempstr)
            drawblack.text((10, 55), tempstr, font=font20, fill=0)
            drawred.text((10 + w4, 55), "'", font=fontweather_small, fill=0)
            drawblack.text((140, 55), str("{0}{1} | {2}{3}".format(int(round(temperature['temp_min'])), u'\u00b0',
                                                                   int(round(temperature['temp_max'])), u'\u00b0')),
                           font=font20, fill=0)

            drawblack.text((10, 75), str("{} hPA".format(int(round(pressure['press'])))), font=font16, fill=0)
            drawblack.text((140, 75), str("{}% RH".format(int(round(humidity)))), font=font16, fill=0)

            drawred.text((5, 85), "A", font=fontweather, fill=0)
            drawred.text((125, 85), "J", font=fontweather, fill=0)
            drawblack.text((30, 90), time.strftime('%I:%M %p', time.localtime(sunrise)), font=font16, fill=0)
            drawblack.text((150, 90), time.strftime('%I:%M %p', time.localtime(sunset)), font=font16, fill=0)

            #draw = draw.transpose(Image.ROTATE_180)

            HBlackimage = HBlackimage.rotate(180.0, expand=1)
            HRedimage = HRedimage.rotate(180.0, expand=1)

            epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
            time.sleep(2)

            epd.sleep()

        except IOError as e:
            print('traceback.format_exc():\n%s', traceback.format_exc())
            epdconfig.module_init()
            epdconfig.module_exit()
            exit()

        # Sleep for 10 minutes - loop will continue after 10 minutes    
        time.sleep(300)  # Wake up every 10 minutes to update weather display


# gracefully exit without a big exception message if possible
def ctrl_c_handler(signal, frame):
    print('Goodbye!')
    # XXX : TODO
    #
    # To preserve the life of the ePaper display, it is best not to keep it powered up -
    # instead putting it to sleep when done displaying, or cutting off power to it altogether.
    #
    # epdconfig.module_exit() shuts off power to the module and calls GPIO.cleanup()
    # The latest epd library chooses to shut off power (call module_exit) even when calling epd.sleep()    
    # epd.sleep() calls epdconfig.module_exit(), which in turns calls cleanup().
    # We can therefore end up in a situation calling GPIO.cleanup twice
    # 
    # Need to cleanup Waveshare epd code to call GPIO.cleanup() only once
    # for now, calling epdconfig.module_init() to set up GPIO before calling module_exit to make sure
    # power to the ePaper display is cut off on exit
    # I have also modified epdconfig.py to initialize SPI handle in module_init() (vs. at the global scope)
    # because slepe/module_exit closes the SPI handle, which wasn't getting initialized in module_init
    epdconfig.module_init()
    epdconfig.module_exit()
    exit(0)


signal.signal(signal.SIGINT, ctrl_c_handler)

if __name__ == '__main__':
    main()
