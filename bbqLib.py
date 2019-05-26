'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import datetime
import json
import random

host = "a3hmttw9ko9d2j.iot.us-east-1.amazonaws.com"
rootCAPath = "root-CA.pem"
certificatePath = "137a61289a-certificate.pem.crt"
privateKeyPath = "137a61289a-private.pem.key"
topic = "bbqData/123"
mode = "publish"
clientId = "basicPubSub"
port = 8883

def initIotClient():
    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
    
    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    
    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    return myAWSIoTMQTTClient

def pubBbqTopic(myAWSIoTMQTTClient, topic, message):    
    # Publish to the same topic in a loop forever

    try:
        myAWSIoTMQTTClient.publish(topic, message, 1)
        print('Published topic %s: %s\n' % (topic, message))
    except:
        print("err no connection")



def main():
    myIOTClient = initIotClient()
    while True:
        data = {}
        data['dateTime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['meatTemp1'] = random.randint(75, 150)
        data['eggTemp1'] = random.randint(150, 300)
        dataJson = json.dumps(data)
        pubBbqTopic(myIOTClient, topic, dataJson)

        time.sleep(1)
    
if __name__ == "__main__":
   main()
