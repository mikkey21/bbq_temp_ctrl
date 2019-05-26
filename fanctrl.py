import os
import time                                  #import the time module
import piplates.MOTORplate as MOTOR          #import the MOTORplate module
import piplates.DAQCplate as DAQC

def getOSTemp():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    print("temp is {0}".format(temp)) #Uncomment here for testing
    return temp

def getTemp():
    temp = DAQC.getTEMP(1,0,'f')
    print "temp: ", temp
    return temp

def setup():
    #configure dc motor 2 on the MOTORplate at address 0 being configured for clockwise
    #motion at a 50% duty cycle and 2.5 seconds of acceleration 
    MOTOR.dcCONFIG(0,1,'cw',100.0,2.5)

def fanOn():    
    #Start DC motor
    MOTOR.dcSTART(0,1)
    time.sleep(2)
    print "Fan Start"              #print notice
def fanOff():
    MOTOR.dcSTOP(0,1)                            #stop the motor
    print "Fan Stop"              #print notice
def setFanSpeed(speed):
    MOTOR.dcSPEED(0,1,speed)                     #increase speed to 100%
    print "Set Fan Speed: ", speed              #print notice

try:
    setup()
    #curr_temp = getTemp()
    set_point = 78
    fanOn()
    fanState = True
    while True:
#        last_temp = curr_temp
#        curr_temp = getTemp()

#        if curr_temp > set_point:
#            fanOn()
#        if curr_temp < set_point:
#            fanOff()
        time.sleep(3)

        
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    MOTOR.dcSTOP(0,1)
    print "Fan Stopped"



#import piplates.MOTORplate as MOTOR          #import the MOTORplate module
#MOTOR.dcCONFIG(0,1,'cw',100.0,2.5)
#MOTOR.dcSTART(0,1)
#MOTOR.dcSTOP(0,1)                            #stop the motor
#print "Fan Stop"              #print notice
