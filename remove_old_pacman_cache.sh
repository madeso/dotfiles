#!/bin/sh
du -h /var/cache/pacman
paccache -r
du -h /var/cache/pacman

