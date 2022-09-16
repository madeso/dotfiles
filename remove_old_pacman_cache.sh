#!/bin/sh
du -h /var/cache/pacman
paccache -rk1
du -h /var/cache/pacman

