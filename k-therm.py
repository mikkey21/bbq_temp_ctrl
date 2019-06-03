
import os
import time
import motctrl
import logging
import bbqLib
import json
import datetime
import re

import therm_api
    
def main():
    logging.basicConfig(level=logging.DEBUG,filename='grill.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

    adc=therm_api.initThermometer()
    
    motctrl.setup()
    avg_temp = therm_api.get_bbq_temp(adc)
    set_point = 245
    alarm_high = 425
    alarm_low = 260

    # set up IOT publish
    myIOTClient = bbqLib.initIotClient()
    topic = "bbqData/123"

    while True:

        time.sleep(5)

        meat_temp1 = therm_api.get_meat_temp1(adc)
        meat_temp2 = therm_api.get_meat_temp2(adc)

        curr_temp = therm_api.get_bbq_temp(adc)

        # Use CPU temp to test temp control
        # note this is cooling when we turn on fan, not heating
        avg_temp = 9*avg_temp/10 + 1*curr_temp/10
        
        if (avg_temp > set_point) or (curr_temp > set_point):
            motctrl.stop_fan()
            fan_state = 'off'
        else:
            motctrl.start_fan()
            fan_state = 'on'

        print "meat_temp1: ",meat_temp1, "meat_temp2: ",meat_temp2
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
        data['meatCurrTemp1'] = round(meat_temp1, 2)
        data['meatCurrTemp2'] = round(meat_temp2, 2)
        data['eggAvgTemp'] = round(avg_temp, 2)
        data['fanState'] = fan_state
        data['setPoint'] = round(set_point,2)
        
        dataJson = json.dumps(data)+"\n"
        bbqLib.pubBbqTopic(myIOTClient, topic, dataJson)

if __name__ == "__main__":
   main()
