#!/bin/sh
#################################################################
#    General
#
# Run this file with sudo
# it will enable and setup system
#
# note: header comments are indented with 3 spaces


#################################################################
#    randr/multimonitor
#
# https://wiki.archlinux.org/index.php/Xrandr
sudo pacman -S arandr autorandr
systemctl enable autorandr.service
# use arandr to setup monitors, and "autorandr --save profilename" to save profiles


#################################################################
#    ntfs usb mounting
sudo pacman -S diskie ntfs-3g


#################################################################
#    Time synchronisation
#  
# https://wiki.archlinux.org/index.php/Systemd-timesyncd
systemctl enable systemd-timesyncd.service
timedatectl set-ntp true


#################################################################
#    ssh agent
#  
cp ssh-agent.service ~/.config/systemd/user/ssh-agent.service
systemctl --user enable ssh-agent.service


#################################################################
#   Display manager (login)
#  
systemctl enable lightdm.service

