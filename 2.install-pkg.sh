#!/bin/zsh
# src: https://wiki.archlinux.org/index.php/Pacman/Tips_and_tricks#Install_packages_from_a_list
pacman -S --needed $(comm -12 <(pacman -Slq | sort) <(sort pkglist.txt))
pip install pystache
