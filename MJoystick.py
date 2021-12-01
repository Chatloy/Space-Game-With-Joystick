import RPi.GPIO as GPIO
import time
from ADCDevice import *

Z_Pin = 12
adc = ADCDevice()

X = 150
Y = 150
Z = 0

def setup():
    global adc
    if adc.detectI2C(0x48):
        adc = PCF8591()
        print("PCF")
    elif adc.detectI2C(0x4b):
        adc = ADS7830()
        print("ADS")
    else:
        print("no device found")
        setup()
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Z_Pin, GPIO.IN, GPIO.PUD_UP)

def loop():
    #while True:
    global X, Y, Z

    val_z = GPIO.input(Z_Pin)
    val_y = adc.analogRead(2)
    val_x = adc.analogRead(0)
    val_q = adc.analogRead(4)
    X = val_x
    Y = val_y
    Z = val_z
    #print("X value: %d \t y value: %d \t z value %d \t q value %d" % (val_x, val_y, val_z, val_q))
    time.sleep(0.01)

def destroy():
    adc.close()
    GPIO.cleanup()

if __name__ == "__main__":
    print("Program is starting...\n")
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        print("\ngoodbye")
