#!/bin/sh
mkdir -p ~/Pictures/
maim -i $(xdotool getactivewindow) ~/Pictures/$(date "+%Y-%m-%d_%H-%M-%S").png

