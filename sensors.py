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


def print_temp_please(id, struct):
    # print(struct)
    max = [-1]
    temp = struct['temp{}_input'.format(id)]
    # find the lowest max that is above 0
    def set_max(n):
        name = 'temp{}_{}'.format(id, n)
        if name in struct:
            t = struct[name]
            if t > 0:
                if max[0] < 0 or t < max[0]:
                    max[0] = t
    set_max('crit')
    set_max('crit_hyst')
    set_max('max')
    set_max('crit_alarm')
    print(temp, max)


def print_temp(struct):
    for i in range(1, 3):
        if 'temp{}_input'.format(i) in struct:
            print_temp_please(i, struct)
            return
    print('error in print_temp')


def print_adapter(name, adapter):
    # print(name)
    # print(adapter)
    printed = 0
    for i in range(1,100):
        name = 'temp{}'.format(i)
        if name not in adapter:
            break
        printed += 1
        print_temp(adapter[name])

    for i in range(0,100):
        name = 'Core {}'.format(i)
        if name not in adapter:
            break
        printed += 1
        print_temp(adapter[name])

    if printed == 0:
        print('error')


def main():
    parser = argparse.ArgumentParser(description='sensors script')
    args = parser.parse_args()

    source = subprocess.check_output(['sensors', '-j'], encoding='UTF-8')
    data = json.loads(source)
    for key in data:
        print_adapter(key, data[key])

if __name__ == "__main__":
    main()

