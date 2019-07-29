#!/bin/sh
maim -st 9999999 | convert - \( +clone -background black -shadow 80x3+5+5 \) +swap -background none -layers merge +repage png:- | xclip -selection clipboard -t image/png

