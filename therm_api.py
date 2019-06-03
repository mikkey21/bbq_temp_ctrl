# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain

# 190  24270
# 184  24183
# 150  25281
# 132  25670
# 99   26060
# 89   26110
# 78   26188
# 72   26221

# 100k
# 200 1950
# 156 3975
# 131 5990
# 100 9850

# 10k
# 200 11730
# 156 16930
# 132 19690
# 100 22650

# 1k
# 200 23460
# 156 25045
# 132 25575
# 100 26074

import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15

def initThermometer():
    # Create an ADS1115 ADC (16-bit) instance.
    adc = Adafruit_ADS1x15.ADS1115()
    return adc
    print ('Thermometer Init Complete')

def get_v_avg(adc, channel):
    v = []
    for i in range(5):
        v.append(adc.read_adc(channel,gain=1))

    v_avg = sum(v)/float(len(v))
    return v_avg

def get_meat_temp1(adc):
    v1 = get_v_avg(adc, 0) 
    #t1 = -0.0124*v1+205
    #t1 = .0000005*v1*v1-0.01673*v1+213.2
    #t1 = .000000043*v1*v1-.0092*v1+295
    t1 = -.000000188*v1*v1-.00274*v1+256+2
    return t1

def get_meat_temp2(adc):
    v2 = get_v_avg(adc, 1) 
    #t2 = -0.0087*v2+303
    #t2 = .000000043*v2*v2-.0092*v2+295
    t2 = -.0000001737*v2*v2-.00341*v2+263+4
    return t2


def get_bbq_temp(adc):
    vq = get_v_avg(adc, 2) 
    #tq = .000000043*vq*vq-.0092*vq+295
    tq = -.0000001737*vq*vq-.00341*vq+263+2
    return tq

# convert voltage to temperature.
# Assumes a 10k resistor to 3.3v and thermistor to ground
def get_temp(adc,channel):
    v = get_v_avg(adc, channel)
    t = -.000000188*v*v-.00274*v+256+2
    return t

def main():

    adc = initThermometer()

    v = [0]*4
    t = [0]*4
    
    for i in range (4):
        v[i] = get_v_avg(adc,i)
        t[i] = get_temp(adc,i)
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*v))
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*t))
        
    # Pause for half a second.
    time.sleep(1)

if __name__ == "__main__":
   main()
