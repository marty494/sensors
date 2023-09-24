#!/usr/bin/python

import glob
import time
import sensor_modules.sensor_lib as sl

#
# Note. The AWS free tier limits:
# This app calls an API on the AWS Gateway (1 million API calls p.m.)
# The G/W calls a Lambda function (1 million requests p.m.)
# The Lambda function stores the entry in DynamoDB (25 GB)
# The Lambda function uses the SNS service to push a notification 
# to my mobile (1 million publishes p.m.)
#
import sensor_modules.rest_lib as rl

import json
from datetime import datetime

# Necessary if the emodules aren't loaded at runtime
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

# TEMP_CHECK_FREQUENCY_SEC = 60 * 15 # Check temp every 15 minutes
TEMP_CHECK_FREQUENCY_SEC = 60 * 60 # Check temp every 60 minutes

MIN_ALARM_TEMP = 3.0  # Send ALARM when less than this in celcius
MAX_ALARM_TEMP = 30.0 # Send ALARM when more than this in celcius

BASE_DIR = '/sys/bus/w1/devices/'
DEVICE_FILE = ''


def setup_sensor():
    try:
        global DEVICE_FILE
        DEVICE_DIR = glob.glob(BASE_DIR + '28*')[0]
        DEVICE_FILE = DEVICE_DIR + '/w1_slave'
    except Exception as e:
        sl.handle_fatal_error_and_email('temp', 'setup_sensor(): ' + str(e))
    

def read_temp_celcius_raw():
    try:
        f = open(DEVICE_FILE, 'r')
        lines = f.readlines()
        f.close()
        return lines
    except Exception as e:
        sl.handle_fatal_error_and_email('temp', 'read_temp_celcius_raw(): ' + str(e))

def read_temp_celcius():
    try:
        lines = read_temp_celcius_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_celcius_raw()

        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
    except Exception as e:
        sl.handle_fatal_error_and_email('temp', 'read_temp_celcius(): ' + str(e))


def check_temp_alarms(temp_celcius):
    try:
        if temp_celcius < MIN_ALARM_TEMP:
            rest_payload = build_rest_payload(temp_celcius)
            rl.consume_rest_api('beta', 'temp', 'POST', rest_payload)

        if temp_celcius > MAX_ALARM_TEMP:
            rest_payload = build_rest_payload(temp_celcius)
            rl.consume_rest_api('beta', 'temp', 'POST', rest_payload)

    except Exception as e:
        sl.handle_error_and_email('temp', 'check_temp_alarms() temp_celcius=' + str(temp_celcius) + ': ' + str(e))

    
def build_rest_payload(temp_celcius):
    try:
        now = datetime.now()
        str_date = now.strftime("%Y-%m-%d")
        str_time = now.strftime("%H:%M")

        payload = {
            'date': str_date,
            'time': str_time,
            'celcius': temp_celcius
        }

        return json.dumps(payload)

    except Exception as e:
        sl.handle_fatal_error_and_email('temp', 'build_rest_payload(): ' + str(e))


def main():
    setup_sensor()

    while True:
        current_temp_celcius = read_temp_celcius()
        sl.write_to_file('temp', current_temp_celcius, 'csv')
        check_temp_alarms(current_temp_celcius)
        time.sleep(TEMP_CHECK_FREQUENCY_SEC)

if __name__=="__main__":
    main()     
