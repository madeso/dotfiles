#!/bin/zsh

# for dotfiles tool
# pip install pystache

pacman -S --needed $(./skip-comments.py packages-to-install)

