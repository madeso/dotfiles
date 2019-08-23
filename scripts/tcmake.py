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


def setup_cmake(source, build, type, compiler):
    os.makedirs(build, exist_ok=True)
    # https://stackoverflow.com/questions/7724569/debug-vs-release-in-cmake
    compilerpp = compiler + '++' if compiler == 'clang' else compiler
    subprocess.run(['cmake', '-G', 'Ninja',
        '-D', 'CMAKE_C_COMPILER='+compiler,
        '-D', 'CMAKE_CXX_COMPILER='+compilerpp,
        '-DCMAKE_BUILD_TYPE='+type, source], cwd=build)

def has_cmake(folder):
    return os.path.exists(os.path.join(folder, 'CMakeLists.txt'))


def handle_setup(args):
    wd = os.getcwd()
    if not has_cmake(wd):
        print('Folder does not look like a cmake project, aborting...')
        return

    if args.check_parent:
        if has_cmake(os.path.dirname(wd)):
            print('parent folder has cmake, aborting...')
            return

    build = os.path.join(wd, 'build')
    compilers = []
    if args.clang:
        compilers.append('clang')
    if args.gcc:
        compilers.append('gcc')
    for compiler in compilers:
        extra = '-' + compiler
        if args.debug:
            setup_cmake(wd, os.path.join(build, 'debug'+extra), 'Debug', compiler)
        if args.release:
            setup_cmake(wd, os.path.join(build, 'release'+extra), 'Release', compiler)
    pass


def main():
    parser = argparse.ArgumentParser(description='Opinionated cmake helper tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('setup', help='setup the build folders')
    sub.add_argument('--no-parent-check', dest='check_parent', action='store_false', help="Don't abort if the parent folder contains a cmake file")
    sub.add_argument('--nogcc', dest='gcc', action='store_false', help="Don't setup gcc as a compiler")
    sub.add_argument('--noclang', dest='clang', action='store_false', help="Don't setup clang as a compiler")
    sub.add_argument('--nodebug', dest='debug', action='store_false', help="Don't setup a debug build")
    sub.add_argument('--norelease', dest='release', action='store_false', help="Don't setup a release build")
    sub.set_defaults(func=handle_setup)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

