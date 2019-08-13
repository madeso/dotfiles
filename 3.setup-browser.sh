#!/bin/sh

# important so set before browser is set, otherwise it will not work
unset BROWSER
xdg-settings set default-web-browser firefox.desktop
export BROWSER=firefox

