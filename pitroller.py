#!/usr/bin/python
from gpiozero import MCP3008
from gpiozero import Button
#from time import sleep
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

readings = [0,0,0,0,0,0]
vref = 3.3

button1 = Button(20)
button2 = Button(21)

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 1

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize display library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
padding = 2

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

while True:
    # Read data from ADC
    for x in range(0, 4):
        with MCP3008(channel=x) as reading:
            readings[x] = reading.value

    # Read the button state
    readings[4] = button1.is_active
    readings[5] = button2.is_active

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    if readings[4] and readings[5]:
        image = Image.open('henry.ppm').convert('1')
        disp.image(image)
        disp.display()
        time.sleep(5)
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)

    # Display Raw values
    draw.text((padding, padding), '{:.2f}'.format(readings[0]), font=font, fill=255)
    draw.text((padding, padding+10), '{:.2f}'.format(readings[1]), font=font, fill=255)

    draw.text((width/2+padding, padding), '{:.2f}'.format(readings[2]), font=font, fill=255)
    draw.text((width/2+padding, padding+10), '{:.2f}'.format(readings[3]), font=font, fill=254)

    # draw axis for left stick measurements
    draw.line((0+padding, height/2, width/2-padding, height/2), fill=255)
    draw.line((width/4, padding, width/4, height-padding), fill=255)

    # draw axis for right stick measurements
    draw.line((width/2+padding, height/2, width-padding, height/2), fill=128)
    draw.line((width/4*3, padding, width/4*3, height-padding), fill=255)

    xaxismapper = width/2-padding*2
    yaxismapper = height-padding*2

    # Joystick 1
    # Actual X and Y of joysticks.
    #x1value = ((readings[0]-0.5) * xaxismapper)
    #y1value = ((readings[1]-0.5) * yaxismapper)
    #if readings[4]:
    #    draw.rectangle((width/4-2+x1value, height/2-2-y1value, width/4+2+x1value, height/2+2-y1value), outline=255, fill=255)
    #else:
    #    draw.rectangle((width/4-2+x1value, height/2-2-y1value, width/4+2+x1value, height/2+2-y1value), outline=255, fill=0)


    # Breadboard X and Y of joysticks.
    x1value = ((readings[1] - 0.5) * xaxismapper)
    y1value = ((readings[0] - 0.5) * yaxismapper)
    if readings[4]:
        draw.rectangle((width/4-2+x1value, height/2-2+y1value, width/4+2+x1value, height/2+2+y1value), outline=255, fill=255)
    else:
        draw.rectangle((width/4-2+x1value, height/2-2+y1value, width/4+2+x1value, height/2+2+y1value), outline=255, fill=0)

    # Joystick 2
    # Actual X and Y of joysticks.
    #x2value = ((readings[2]- 0.5) * xaxismapper)
    #y2value = ((readings[3]- 0.5) * yaxismapper)
    #if readings[5]:
    #    draw.rectangle((width/4*3-2+x2value, height/2-2-y2value, width/4*3+2+x2value, height/2+2-y2value), outline=255, fill=255)
    #else:
    #    draw.rectangle((width/4*3-2+x2value, height/2-2-y2value, width/4*3+2+x2value, height/2+2-y2value), outline=255, fill=0)

    # Breadboard X and Y of joysticks.
    x2value = ((readings[3]- 0.5) * xaxismapper)
    y2value = ((readings[2]- 0.5) * yaxismapper)
    if readings[5]:
        draw.rectangle((width/4*3-2+x2value, height/2-2+y2value, width/4*3+2+x2value, height/2+2+y2value), outline=255, fill=255)
    else:
        draw.rectangle((width/4*3-2+x2value, height/2-2+y2value, width/4*3+2+x2value, height/2+2+y2value), outline=255, fill=0)


    # Display image.
    disp.image(image)
    disp.display()

    # Sleep to save the CPU and battery life
    time.sleep(.01)
