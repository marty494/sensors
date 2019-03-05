#!/usr/bin/python

import sensor_modules.sensor_lib as sl

def test_email():
    sl.send_email('Raspberry Pi E-mail Test...', 'E-mail body - TEST');


def main():
    try:
        test_email();

    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__=="__main__":
    main()     
