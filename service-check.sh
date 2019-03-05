#!/bin/sh

echo -n Temperature Sensor: ; sudo systemctl status temp-sensor.service|grep Active
echo -n Regeneration Sensor: ; sudo systemctl status regen-sensor.service|grep Active
echo -n Salt Level Sensor: ; sudo systemctl status salt-sensor.service|grep Active

