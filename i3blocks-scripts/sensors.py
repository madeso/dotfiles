#!/usr/bin/env python3

import argparse
import os
import filecmp
import subprocess
import shutil
import sys
import platform
import typing
import json
import re
from enum import Enum
import random

class Data:
    def __init__(self, args):
        self.args = args
        self.text = []

def message(data, t, m):
    is_hot = t > m
    text = '{0:.1f}'.format(t)
    bg = data.args.hot_bg    if is_hot else data.args.base_bg
    fg = data.args.hot_color if is_hot else data.args.base_color
    data.text.append("<span background='{0}' color='{1}'>{2}</span>".format(bg, fg, text))


def print_temp_please(data, id, struct):
    temp = struct['temp{}_input'.format(id)]
    def var(n):
        name = 'temp{}_{}'.format(id, n)
        if name in struct:
            return struct[name]
        else:
            return -1
    maxes = [t for t in [
                var('crit'),
                var('crit_hyst'),
                var('max'),
                var('crit_alarm')
            ] if t > 0]
    if len(maxes) > 0:
        max_temp = min(maxes)
        message(data, temp, max_temp)
    else:
        message(data, temp, temp+1)


def print_temp(data, struct):
    for i in range(1, 3):
        if 'temp{}_input'.format(i) in struct:
            print_temp_please(data, i, struct)
            return
    if data.args.debug:
        print('error in print_temp')


def print_adapter(data, name, adapter):
    printed = 0
    for i in range(1,100):
        name = 'temp{}'.format(i)
        if name not in adapter:
            break
        printed += 1
        print_temp(data, adapter[name])

    for i in range(0,100):
        name = 'Core {}'.format(i)
        if name not in adapter:
            break
        printed += 1
        print_temp(data, adapter[name])

    if printed == 0:
        if data.args.debug:
            print('error')


def main():
    parser = argparse.ArgumentParser(description='sensors script')

    parser.add_argument(
        '-B',
        '--base_bg',
        default='white',
        help='base background of the output'
    )
    parser.add_argument(
        '-U',
        '--updates_available_bg',
        default='red',
        help='color of the background, when updates are available(default=white)'
    )
    parser.add_argument(
        '-b',
        '--base_color',
        default='black',
        help='base color of the text'
    )
    parser.add_argument(
        '-u',
        '--updates_available_color',
        default='white',
        help='color of the text, when updates are available'
    )
    parser.add_argument('-d', '--debug', action='store_true',
        help='add debugability to the command')

    args = parser.parse_args()

    data = Data(args)

    source = subprocess.check_output(['sensors', '-j'], encoding='UTF-8')
    sensor_data = json.loads(source)
    for key in sensor_data:
        print_adapter(data, key, sensor_data[key])

    print(' '.join(data.text))

if __name__ == "__main__":
    main()

