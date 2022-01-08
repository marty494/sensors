#!/usr/bin/python

import glob
import time
import sensor_modules.sensor_lib as sl
import sensor_modules.rest_lib as rl
import json
from datetime import datetime

# Necessary if the emodules aren't loaded at runtime
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

# TEMP_CHECK_FREQUENCY_SEC = 60 * 15 # Check temp every 15 minutes
TEMP_CHECK_FREQUENCY_SEC = 60 * 60 # Check temp every 60 minutes

MIN_ALARM_TEMP = 4.0  # Send ALARM when less than this in celcius
MAX_ALARM_TEMP = 30.0 # Send ALARM when more than this in celcius

BASE_DIR = '/sys/bus/w1/devices/'
DEVICE_FILE = ''


def setup_sensor():
    try:
        global DEVICE_FILE
        DEVICE_DIR = glob.glob(BASE_DIR + '28*')[0]
        DEVICE_FILE = DEVICE_DIR + '/w1_slave'
    except:
        sl.handle_fatal_error_and_email('temp', 'setup_sensor()')
    

def read_temp_celcius_raw():
    try:
        f = open(DEVICE_FILE, 'r')
        lines = f.readlines()
        f.close()
        return lines
    except:
        sl.handle_fatal_error_and_email('temp', 'read_temp_celcius_raw()')

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
    except:
        sl.handle_fatal_error_and_email('temp', 'read_temp_celcius()')


def check_temp_alarms(temp_celcius):
    try:
        if temp_celcius < MIN_ALARM_TEMP:
            rest_payload = build_rest_payload(temp_celcius)
            rl.consume_rest_api('beta', 'temp', 'POST', rest_payload)

            # sl.send_email('Min Temperature EXCEEDED...', 
            # 'Temperature: ' + str(temp_celcius) + 
            # 'C has EXCEEDED: ' + str(MIN_ALARM_TEMP) + 'C')

        if temp_celcius > MAX_ALARM_TEMP:
            rest_payload = build_rest_payload(temp_celcius)
            rl.consume_rest_api('beta', 'temp', 'POST', rest_payload)

            # sl.send_email('Max Temperature EXCEEDED...', 
            # 'Temperature: ' + str(temp_celcius) + 
            # 'C has EXCEEDED: ' + str(MAX_ALARM_TEMP) + 'C')
    except:
        sl.handle_error_and_email('temp', 'check_temp_alarms() temp_celcius=' + str(temp_celcius))

    
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

    except:
        sl.handle_fatal_error_and_email('temp', 'build_rest_payload()')


def main():
    setup_sensor()

    while True:
        current_temp_celcius = read_temp_celcius()
        sl.write_to_file('temp', current_temp_celcius, 'csv')
        check_temp_alarms(current_temp_celcius)
        time.sleep(TEMP_CHECK_FREQUENCY_SEC)

if __name__=="__main__":
    main()     
