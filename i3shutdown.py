#!/usr/bin/env python

import rofi

mess = {}
mess['lock'] = ['i3lock']
mess['exit'] = ['i3-msg exit']
mess['suspend'] = ['systemctl', 'suspend']
mess['hibernate'] = ['systemctl', 'hibernate']
mess['reboot'] = ['systemctl', 'reboot']
mess['shutdown'] = ['systemctl', 'poweroff']

rofi.cmd(mess)
