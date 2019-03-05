#!/usr/bin/python

import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008 as ADC

CLK = 12 # GPIO 18 = Pin 12 (CLK -> CLK)
MISO = 7 # GPIO 23 = Pin 16 (DOUT -> MISO)
MOSI = 8 # GPIO 24 = Pin 18 (DIN -> MOSI)
CS = 25 # GPIO 25 = Pin 22 (CS -> CE0)

mcp = ADC.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


def get_voltage():
    v = (mcp.read_adc(0) / 1023.0) * 3.3
    return v

def calc_distance_cm(v):
    a = 0.00385
    b = -0.2205
    c = 4.12

    cm = ((b*-1) + (((b**2)-(4*a*c))*0.5)) / (2*a)
    return cm


if __name__ == '__main__':
    total_volt = 0
    total_samples = 0

    while True:
        volt = get_voltage()
        cm = calc_distance_cm(volt)

        total_volt = total_volt + volt
        total_samples = total_samples + 1
        avg_volt = total_volt / total_samples

        print 'voltage {:.2f}V, distance {:.2f}cm, average voltage: {:.2f}V'.format(volt, cm, avg_volt)

        per = (volt-1.23)*111
        if per < 0: per = 0
        if per > 100: per = 100
        per = round(per, 2)
        print str(per) + '% full'

        time.sleep(1)
