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
from enum import Enum

SSH_CONFIG = os.path.join(os.path.expanduser('~'), '.ssh', 'config')

def run(args):
    lines = []
    if os.path.isfile(SSH_CONFIG):
        with open(SSH_CONFIG) as f:
            lines = [line.rstrip('\n') for line in f]
    wanted_properties = {
        'AddKeysToAgent': 'yes',
        'UserKnownHostsFile': '~/.ssh/known_hosts'
    }
    read_prop = {p:False for p in wanted_properties}

    newlines = []
    for l in lines:
        nl = l
        prop = l.strip().split()
        if args.debug:
            print(l)
            print(prop)
        property = prop[0] if len(prop)>0 else ''
        if property in wanted_properties:
            nl = '{} {}'.format(property, wanted_properties[property])
            read_prop[property] = True
            if args.debug:
                print('REPLACED {}'.format(property))
        newlines.append(nl)

    missing_properties = ['{} {}'.format(prop, wanted_properties[prop])
            for prop in wanted_properties if not read_prop[prop]]

    if args.debug:
        print('missing properties: {}'.format(missing_properties))

    newlines = missing_properties + newlines

    if newlines[-1:][0].strip() != '':
        newlines.append('')
        if args.debug:
            print('ADDING NEWLINE AT END')

    if args.debug:
        print('RUN DONE')
    return newlines

def handle_test(args):
    data = run(args)
    for d in data:
        print(d)


def handle_update(args):
    data = run(args)
    with open(SSH_CONFIG, 'w') as f:
        for l in data:
            f.write('{}\n'.format(l))


def main():
    parser = argparse.ArgumentParser(description='Update ssh config to my prefered settings')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('test', help="Do everything but don't write")
    sub.add_argument('--debug', action='store_true', help='Debug the code')
    sub.set_defaults(func=handle_test)

    sub = sub_parsers.add_parser('update', help='Update ssh config')
    sub.add_argument('--debug', action='store_true', help='Debug the code')
    sub.set_defaults(func=handle_update)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
