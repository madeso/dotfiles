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

def aur_path():
    return os.path.expanduser('~/aur/')


def find_git_folders(aur):
    r = []
    for e in os.listdir(aur):
        p = os.path.join(aur, e)
        if os.path.isdir(p):
            if os.path.isdir(os.path.join(p, '.git')):
                r.append(p)
    return r


def cmd(cmd, cwd):
    return subprocess.check_output(cmd, cwd=cwd).decode('utf8').strip()

def git_local(cwd):
    return cmd(['git', 'rev-parse', '@'], cwd)

def git_remote(cwd):
    return cmd(['git', 'rev-parse', '@{u}'], cwd)

def git_base(cwd):
    return cmd(['git', 'merge-base', '@', '@{u}'], cwd)

def git_info(cwd):
    local = git_local(cwd)
    remote = git_remote(cwd)
    base = git_base(cwd)
    if local == remote:
        return 'Up to date'
    elif local == base:
        return 'Need to pull'
    elif remote == base:
        return 'Need to push'
    else:
        return 'Diverged'

#############################################################################

def handle_ls(args):
    aur = aur_path()
    print(aur)

    projects = find_git_folders(aur)
    for p in projects:
        print(p, git_info(p))


def main():
    parser = argparse.ArgumentParser(description='aur helper tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('ls', aliases=['dir'], help='list aur libraries')
    sub.set_defaults(func=handle_ls)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

