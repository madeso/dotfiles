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
import urllib.request


# src: https://stackoverflow.com/questions/7243750/download-file-from-web-in-python-3
def download(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    return text


def get_mirrors():
    lines = download('https://www.archlinux.org/mirrorlist/?ip_version=6').splitlines()
    country = []
    name = ''
    added = False
    intro = []
    mirrors = {}
    for l in lines:
        if l.strip().startswith('##'):
            if name!='' and len(country) > 0:
                mirrors[name] = country
                country = []
                if not added and len(intro) > 0:
                    del intro[-1]
                added = True
            name = l.strip()[2:].strip().lower()
            if not added:
                intro.append(l)
        elif l.strip().startswith('#Server'):
            country.append(l.strip()[1:])
        elif len(l.strip()) == 0:
            pass
        else:
            print('Unknown line', l)
    if name=='' and len(country) > 0:
        mirrors[name] = country
        country = []
    mirrors['intro'] = intro
    return mirrors


def handle_ls(args):
    mirrors = get_mirrors()
    for m in mirrors.keys():
        print(m)


def handle_write(args):
    # todo: write to /etc/pacman.d/mirrorlist
    mirrors = get_mirrors()
    for l in args.lib:
        if not l.lower() in mirrors:
            print('no country named ', l)
            return

        if l != 'intro':
            print('#', l)
        for c in mirrors[l.lower()]:
            print(c)
        print()


def main():
    parser = argparse.ArgumentParser(description='aur helper tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('ls', help='list countries')
    sub.set_defaults(func=handle_ls)

    sub = sub_parsers.add_parser('write', help='write mirrors')
    sub.add_argument('lib', nargs='+', help='libraries to write')
    sub.set_defaults(func=handle_write)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

