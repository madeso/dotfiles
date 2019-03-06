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


def get_project_name(folder):
    return os.path.basename(folder)


def cmd(cmd, cwd):
    return subprocess.check_output(cmd, cwd=cwd).decode('utf8').strip()

def git_local(cwd):
    return cmd(['git', 'rev-parse', '@'], cwd)

def git_remote(cwd):
    return cmd(['git', 'rev-parse', '@{u}'], cwd)

def git_base(cwd):
    return cmd(['git', 'merge-base', '@', '@{u}'], cwd)

def git_fetch(cwd):
    cmd(['git', 'fetch', '-q'], cwd)


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


pkg_pattern = re.compile(r'([a-zA-Z_0-9]*depends[a-zA-Z_0-9]*) *=\(([^)]*)\)')
string_patterns = [
        re.compile(r'\"([^"]*)\"'),
        re.compile(r"\'([^']*)\'")
        ]

def pkg_info(folder):
    file = os.path.join(folder, 'PKGBUILD')
    if not os.path.isfile(file):
        return None
    with open(file, 'r') as f:
        items = pkg_pattern.finditer(f.read())
        for found in items:
            var = found.group(1)
            libs = found.group(2)
            print(var, ':')
            for pat in string_patterns:
                for slib in pat.finditer(libs):
                    print(slib)
    return []


#############################################################################

def handle_ls(args):
    aur = aur_path()
    # print(aur)

    projects = find_git_folders(aur)
    for p in projects:
        name = get_project_name(p)
        print(name)
        print('Git:', git_info(p))
        pkg_info(p)
        print()
        

def handle_check(args):
    aur = aur_path()

    projects = find_git_folders(aur)
    for p in projects:
        git_fetch(p)
        print(p, git_info(p))
        # parse PKGBUILD for dependencies
        # use pacman -Qi package to check if dependency has been updated


def main():
    parser = argparse.ArgumentParser(description='aur helper tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('ls', aliases=['dir'], help='list aur libraries')
    sub.set_defaults(func=handle_ls)

    sub = sub_parsers.add_parser('check', aliases=['ch'], help='list aur libraries')
    sub.set_defaults(func=handle_check)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

