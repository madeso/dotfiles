#!/bin/sh
# if no mattery is available, the BAT0 folder doesn't exist
cat /sys/class/power_supply/BAT0/capacity
cat /sys/class/power_supply/BAT0/status

