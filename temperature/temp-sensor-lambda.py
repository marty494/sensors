#!/usr/bin/python

import sensor_modules.rest_lib as rl
import sensor_modules.sensor_lib as sl
import glob
import time
import json
from datetime import datetime


# Necessary if the emodules aren't loaded at runtime
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

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

def build_rest_payload():
    # '{"date": "2022-01-08", "time": "17:59", "celcius": 5.590}'
    try:
        now = datetime.now()
        str_date = now.strftime("%Y-%m-%d")
        str_time = now.strftime("%H:%M")
        celcius = read_temp_celcius()

        payload = {
            'date': str_date,
            'time': str_time,
            'celcius': celcius
        }

        return json.dumps(payload)

    except:
        sl.handle_fatal_error_and_email('temp', 'build_rest_payload()')


def main():
    setup_sensor()
    rest_payload = build_rest_payload()
    rl.consume_rest_api('beta', 'temp', 'POST', rest_payload)

if __name__=="__main__":
    main()
