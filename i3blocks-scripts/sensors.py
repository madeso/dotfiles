#!/usr/bin/env python3

import argparse
import subprocess
import typing
import json


class Data:
    def __init__(self, args):
        self.args = args
        self.text = []

    def message_print(self, current_temp: float, max_temp: float):
        is_hot = current_temp > max_temp
        text = '{0:.1f}'.format(current_temp)
        bg = self.args.hot_bg    if is_hot else self.args.base_bg
        fg = self.args.hot_color if is_hot else self.args.base_color
        self.text.append("<span background='{0}' color='{1}'>{2}</span>".format(bg, fg, text))
    
    def message_debug(self, current_temp: float, max_temp: float):
        is_hot = current_temp > max_temp
        self.text.append("{0:.1f} / {1:.1f} => {2}".format(current_temp, max_temp, is_hot))

    def message(self, current_temp: float, max_temp: float):
        if self.args.debug:
            self.message_debug(current_temp, max_temp)
        else:
            self.message_print(current_temp, max_temp)


def print_temp_please(data: Data, temp_id, struct):
    temp = struct['temp{}_input'.format(temp_id)]
    def var(n):
        name = 'temp{}_{}'.format(temp_id, n)
        if name in struct:
            return struct[name]
        else:
            return -1
    all_max_temps = [var('crit'), var('crit_hyst'), var('max'), var('crit_alarm')]
    # some temps are as low as 5
    max_temps = [t for t in all_max_temps if t > 10]
    if len(max_temps) > 0:
        max_temp = min(max_temps)
        data.message(temp, max_temp)
    else:
        data.message(temp, temp+1)


def print_temp(data: Data, struct):
    for i in range(1, 9):
        if 'temp{}_input'.format(i) in struct:
            print_temp_please(data, i, struct)
            return
    if data.args.debug:
        print('error in print_temp')


def print_adapter(data: Data, name: str, adapter):
    printed = 0
    for i in range(1, 100):
        name = 'temp{}'.format(i)
        if name not in adapter:
            break
        printed += 1
        print_temp(data, adapter[name])

    for i in range(0, 100):
        name = 'Core {}'.format(i)
        if name not in adapter:
            break
        printed += 1
        print_temp(data, adapter[name])

    if printed == 0:
        if data.args.debug:
            print('error')


def handle_print(args):
    data = Data(args)
    source = subprocess.check_output(['sensors', '-j'], encoding='UTF-8')
    sensor_data = json.loads(source)
    for key in sensor_data:
        print_adapter(data, key, sensor_data[key])

    if args.debug:
        print('\n'.join(data.text))
    else:
        print(' '.join(data.text))


def main():
    parser = argparse.ArgumentParser(description='sensors script')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', metavar='<command>')

    sub = sub_parsers.add_parser('print', help='Copy files to HOME')
    sub.add_argument(
        '-B',
        '--base_bg',
        default='white',
        help='base background of the output'
    )
    sub.add_argument(
        '-U',
        '--hot_bg',
        default='red',
        help='color of the background, when updates are available(default=white)'
    )
    sub.add_argument(
        '-b',
        '--base_color',
        default='black',
        help='base color of the text'
    )
    sub.add_argument(
        '-u',
        '--hot_color',
        default='white',
        help='color of the text, when updates are available'
    )
    sub.add_argument('-d', '--debug', action='store_true',
                     help='add debugability to the command')
    sub.set_defaults(func=handle_print)

    args = parser.parse_args()

    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
