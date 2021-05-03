#!/usr/bin/python

import time
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008 as ADC

import sensor_modules.sensor_lib as sl

CLK = 12 # GPIO 18 = Pin 12 (CLK -> CLK)
MISO = 7 # GPIO 23 = Pin 16 (DOUT -> MISO)
MOSI = 8 # GPIO 24 = Pin 18 (DIN -> MOSI)
CS = 25 # GPIO 25 = Pin 22 (CS -> CE0)

mcp = ADC.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

SALT_CHECK_FREQUENCY_SEC = 3600
FULL_VOLTAGE = 2.3
EMPTY_VOLTAGE = 1.0
VOLTAGE_RANGE = FULL_VOLTAGE - EMPTY_VOLTAGE
LOW_SALT_PERCENTAGE = 25

low_email_sent_date = datetime.today().date() - timedelta(days=1)
empty_email_sent_date = datetime.today().date() - timedelta(days=1)
status_email_sent_date = datetime.today().date() - timedelta(days=1)

def get_voltage():
    return (mcp.read_adc(0) / 1023.0) * 3.3


def salt_update(salt_level):
    global low_email_sent_date
    global empty_email_sent_date
    global status_email_sent_date

    try:
        results = str(salt_level)

        sl.write_to_file('salt', results, 'csv')

        if salt_level == 0:
            if empty_email_sent_date < datetime.today().date():
                empty_email_sent_date = datetime.today().date()
                sl.send_email('Salt Empty...', 'Water Softener salt is empty - refill now') 
                # print str(empty_email_sent_date) + ': SEND EMAIL: SALT EMPTY'
    
        elif salt_level <= LOW_SALT_PERCENTAGE:
            if low_email_sent_date < datetime.today().date():
                low_email_sent_date = datetime.today().date()
                sl.send_email('Salt Low...', 'Water Softener salt is low: ' + str(round(salt_level,1)) + '% remaining') 
                # print str(low_email_sent_date) + ': SEND EMAIL: SALT LOW: ' + str(round(salt_level,1)) + '% remaining'

        else:
            if status_email_sent_date < datetime.today().date():
                status_email_sent_date = datetime.today().date()
                sl.send_email('Salt Level Update...', 'Water Softener salt level is: ' + str(round(salt_level,1)) + '% remaining')

    except:
        sl.handle_fatal_error_and_email('salt', 'salt_update() salt_level="' + str(salt_level) + '"')


def salt_check():
    volt = get_voltage()
    per = (volt - EMPTY_VOLTAGE) / VOLTAGE_RANGE * 100
    if per <= 0:
        per = 0
    elif per > 100:
        per = 100

    print str(round(volt,1)) + 'V = ' + str(round(per,1)) + '% Remaining'

    return per
    

def main():
    try:
        while True :
            salt_update(salt_check())
            time.sleep(SALT_CHECK_FREQUENCY_SEC)

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__=="__main__":
    main()   
