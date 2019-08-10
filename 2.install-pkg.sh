#!/bin/zsh
pacman -S --needed `comm -12 <(pacman -Slq | sort) <(sort pkglist.txt)`
