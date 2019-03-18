#!/usr/bin/python

import time
import datetime
import RPi.GPIO as GPIO

import sensor_modules.sensor_lib as sl

# Necessary if the emodules aren't loaded at runtime
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

FLOW_CHECK_FREQUENCY_SEC = 0.1
FINISH_WAIT_SEC = 60 # How many seconds of no activity to determine regen finish
MINIMUM_DURATION_SEC = 60 # Ignore regen duration less than this duration as they are not genuine

start_timestamp = 0
last_timestamp = 0

def sensor_callback(channel):
    if last_timestamp == 0:
        regen_start()
    else:
        regen_update()
    
    # Not needed: Used to help determine flow RATE    
    # if GPIO.input(channel):
        # No magnet
        # print("Sensor HIGH " + stamp)
    # else:
        # Magnet
        # print("Sensor LOW " + stamp)


def regen_start():
    try:
        global start_timestamp
        global last_timestamp

        timestamp = time.time()
        start_timestamp = timestamp
        last_timestamp = timestamp
    except:
        sl.handle_fatal_error_and_email('regen', 'regen_start() timestamp=' + str(timestamp))


def regen_update():
    try:
        global last_timestamp
        last_timestamp = time.time()
    except:
        sl.handle_fatal_error_and_email('regen', 'regen_update() last_timestamp=' + str(last_timestamp))
        

def regen_finish(timestamp):
    try:
        global start_timestamp
        global last_timestamp

        duration = last_timestamp - start_timestamp

        start_stamp = datetime.datetime.fromtimestamp(start_timestamp).strftime('%H:%M:%S')
        finish_stamp = datetime.datetime.fromtimestamp(last_timestamp).strftime('%H:%M:%S')
        results = start_stamp + ',' + finish_stamp + ',' + str(duration)

        start_timestamp = 0
        last_timestamp = 0

        if duration < MINIMUM_DURATION_SEC: 
            sl.write_to_file('regen-skipped', results, 'csv')

        else:
            sl.write_to_file('regen', results, 'csv')
            sl.send_email('Regeneration complete...', 
                'Regeneration: Start = ' + start_stamp + ', ' +
                'Finish: ' + finish_stamp + ', ' +
                'Duration: ' + str(duration) + ' seconds')

    except:
        sl.handle_fatal_error_and_email('regen', 'regen_finish() results="' + results + '"')


def setup_sensor():
    try:
        GPIO.setmode(GPIO.BCM)

        # Set Switch GPIO as input and Pull high by default
        GPIO.setup(14 , GPIO.IN)
        GPIO.add_event_detect(14, GPIO.FALLING, callback=sensor_callback, bouncetime=200)
    except:
        sl.handle_fatal_error_and_email('regen', 'setup_sensor()')


def regen_check():
    if start_timestamp != 0:
        timestamp = time.time()
        if timestamp - last_timestamp > FINISH_WAIT_SEC:
            regen_finish(timestamp)
        

def main():
    setup_sensor()

    try:
        while True :
            time.sleep(FLOW_CHECK_FREQUENCY_SEC)
            regen_check();

    except KeyboardInterrupt:
        GPIO.cleanup()



if __name__=="__main__":
    main()     
