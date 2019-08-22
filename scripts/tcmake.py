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


def setup_cmake(source, build, type):
    os.makedirs(build, exist_ok=True)
    # https://stackoverflow.com/questions/7724569/debug-vs-release-in-cmake
    subprocess.run(['cmake', '-G', 'Ninja', '-DCMAKE_BUILD_TYPE='+type, source], cwd=build)

def handle_setup(args):
    wd = os.getcwd()
    setup_cmake(wd, os.path.join(wd, 'debug'), 'Debug')
    setup_cmake(wd, os.path.join(wd, 'release'), 'Release')
    pass


def main():
    parser = argparse.ArgumentParser(description='cmake helper tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('setup', help='setup the build folders')
    sub.set_defaults(func=handle_setup)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

