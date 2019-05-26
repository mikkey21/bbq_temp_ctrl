
# find devices in: /sys/bus/w1/devices
# run with: python k-therm.py -i 28-00000758ddbf
# 28-00000758ddbf  - ds18b20 
# 3b-2c98073dad7b - max31850

import os
import glob
import time
import sys, getopt
import motctrl
import logging
import bbqLib
import json
import datetime
import re

# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')
 
def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def read_cpu_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    matchObj = re.match( r'temp=(\d*\.\d*)',temp)
    t = matchObj.group(1)
    return float(t)
    
def main(argv):
    logging.basicConfig(level=logging.DEBUG,filename='grill.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

    inputfile = ''
    base_dir = '/sys/bus/w1/devices/'
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
    print 'Input file is "', inputfile

    device_folder = base_dir + inputfile 
    device_file = device_folder + '/w1_slave'
    print "device file is: ", device_file
 
    motctrl.setup()
    avg_temp = read_temp(device_file)
    #avg_temp = read_cpu_temp()
    set_point = 275
    alarm_high = 425
    alarm_low = 260


    # set up IOT publish
    myIOTClient = bbqLib.initIotClient()
    topic = "bbqData/123"

    while True:

        time.sleep(1)

        curr_temp = read_temp(device_file)

        # Use CPU temp to test temp control
        # note this is cooling when we turn on fan, not heating
        #curr_temp = read_cpu_temp()
        avg_temp = 9*avg_temp/10 + 1*curr_temp/10

        
        if (avg_temp > set_point) or (curr_temp > set_point):
            motctrl.stop_fan()
            fan_state = 'off'
        else:
            motctrl.start_fan()
            fan_state = 'on'
            
        log_string = "curr_temp "+str(curr_temp)+"avg_temp: "+str(avg_temp)+"fan_state: "+str(fan_state)
        print log_string
        logging.info(log_string)

        if avg_temp > alarm_high:
            log_string = "HIGH TEMP ALARM", str(curr_temp), (avg_temp)
            print log_string
            logging.warning(log_string)

        if avg_temp < alarm_low:
            log_string = "LOW TEMP ALARM", str(curr_temp), str(avg_temp)
            print log_string
            logging.warning(log_string)
        
	data = {}
        data['dateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['eggCurrTemp1'] = round(curr_temp, 2)
        data['eggAvgTemp'] = round(avg_temp, 2)
        data['fanState'] = fan_state
        data['setPoint'] = round(set_point,2)
        
        dataJson = json.dumps(data)+"\n"
        bbqLib.pubBbqTopic(myIOTClient, topic, dataJson)

if __name__ == "__main__":
   main(sys.argv[1:])
