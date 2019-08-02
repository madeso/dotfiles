#!/bin/sh
maim | convert - -scale 25% -blur 0x2 -filter point -scale 400% ~/.lockimg.png && feh ~/.lockimg.png
# maim | convert - -scale 25% -blur 0x2 ~/.lockimg.png && i3lock -i ~/.lockimg.png
