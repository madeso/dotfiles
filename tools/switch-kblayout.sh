#!/bin/bash
pwd >> ~/capslock.txt
(setxkbmap -query | grep -q "layout:\s\+us") && setxkbmap se || setxkbmap us
source ~/dev/dotfiles/tools/setup_capslock.sh
pkill -RTMIN+10 i3blocks
