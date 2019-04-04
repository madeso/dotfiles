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


def handle_search(args):
    subprocess.run(['pacman', '-Ss', args.lib])


def handle_info(args):
    subprocess.run(['pacman', '-Qi', args.lib])


def handle_install(args):
    subprocess.run(['pacman', '-S', args.lib])


# hrm...
def handle_remove(args):
    subprocess.run(['pacman', '-R', args.lib])


def handle_installed(args):
    subprocess.run(['pacman', '-Qe'])


def handle_update(args):
    subprocess.run(['pacman', '-Syu'])

def main():
    parser = argparse.ArgumentParser(description='pacman helper tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('search', help='search for unknown lib')
    sub.add_argument('lib')
    sub.set_defaults(func=handle_search)

    sub = sub_parsers.add_parser('info', help='get info about specific lib')
    sub.add_argument('lib')
    sub.set_defaults(func=handle_info)

    sub = sub_parsers.add_parser('install', help='install lib')
    sub.add_argument('lib')
    sub.set_defaults(func=handle_install)

    sub = sub_parsers.add_parser('remove', help='remove lib')
    sub.add_argument('lib')
    sub.set_defaults(func=handle_remove)

    sub = sub_parsers.add_parser('ls', help='List all explicitly installed packages')
    sub.set_defaults(func=handle_installed)

    sub = sub_parsers.add_parser('update', help='update system')
    sub.set_defaults(func=handle_update)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

