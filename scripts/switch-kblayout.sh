#!/bin/bash
(setxkbmap -query | grep -q "layout:\s\+us") && setxkbmap se || setxkbmap us
source fix-capslock.sh
