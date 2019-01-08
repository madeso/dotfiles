#!/usr/bin/env python

import rofi
import os

mess = {}
mess['lock'] = ['i3lock']
mess['exit'] = ['i3-msg exit']
mess['suspend'] = ['systemctl', 'suspend']
mess['hibernate'] = ['systemctl', 'hibernate']
mess['reboot'] = ['systemctl', 'reboot']
mess['shutdown'] = [os.path.expanduser('~/dev/dotfiles/safe-shutdown.sh')]

rofi.cmd(mess)
