#!/usr/bin/env python

# Import required modules
import time
import RPi.GPIO as GPIO

def setup():
    # Declare the GPIO settings
    GPIO.setmode(GPIO.BOARD)
    # set up GPIO pins
    GPIO.setup(10, GPIO.OUT) # Connected to PWMA
    GPIO.setup(11, GPIO.OUT) # Connected to AIN2
    GPIO.setup(12, GPIO.OUT) # Connected to AIN1
    GPIO.setup(13, GPIO.OUT) # Connected to STBY

def start_fan():
    # Disable STBY (standby)
    GPIO.output(13, GPIO.HIGH)
    # Drive the motor counterclockwise
    GPIO.output(11, GPIO.LOW) # Set AIN1
    GPIO.output(12, GPIO.HIGH) # Set AIN2
    # Set the motor speed
    GPIO.output(10, GPIO.HIGH) # Set PWMA
    print "start fan"

def stop_fan():
    # Reset all the GPIO pins by setting them to LOW
    GPIO.output(12, GPIO.LOW) # Set AIN1
    GPIO.output(11, GPIO.LOW) # Set AIN2
    GPIO.output(10, GPIO.LOW) # Set PWMA
    GPIO.output(13, GPIO.LOW) # Set STBY
    print "stop fan"

def main():
    setup()
    start_fan()
    time.sleep(5)
    stop_fan()
    
if __name__ == "__main__":
    main()
