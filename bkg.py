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

def get_dotfiles():
    return os.path.dirname(os.path.realpath(__file__))


def get_backgrounds():
    return os.path.join(get_dotfiles(), 'backgrounds')


def list_files(dir):
    return [os.path.join(dir, f) for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    
def handle_ls(args):
    bkg = get_backgrounds()
    print('bkg:', bkg)

    files = list_files(bkg)
    for file in files:
        print('  ', file)

def handle_set(args):
    files = list_files(get_backgrounds())
    f = random.choice(files)
    print('setting random bkg:', f)
    subprocess.run(['feh', '--bg-scale', f])

def main():
    parser = argparse.ArgumentParser(description='bkg helper tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('ls', help='list images')
    sub.set_defaults(func=handle_ls)
    
    sub = sub_parsers.add_parser('set', help='set background')
    sub.set_defaults(func=handle_set)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

