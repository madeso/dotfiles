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
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT, cwd=cwd).decode('utf8').strip()

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

version_pattern = re.compile(r'Version\s*:\s*(\S*)')
def installed_version(pkg, cwd):
    try:
        out = cmd(['pacman', '-Qi', pkg], cwd)
        for p in version_pattern.finditer(out):
            return p.group(1)
        return None
    except subprocess.CalledProcessError:
        return None


class Pkg:
    def __init__(self, pkg, version):
        self.pkg = pkg
        self.version = version


pkg_pattern = re.compile(r'([a-zA-Z_0-9]*depends[a-zA-Z_0-9]*) *=\(([^)]*)\)')
string_patterns = [
        re.compile(r'\"\s*([\-\.a-zA-Z0-9]+)[^"]*\"'),
        re.compile(r"'\s*([\-\.a-zA-Z0-9]+)[^']*'")
        ]

def pkg_info(folder):
    file = os.path.join(folder, 'PKGBUILD')
    if not os.path.isfile(file):
        return None
    ret = {}
    with open(file, 'r') as f:
        items = pkg_pattern.finditer(f.read())
        for found in items:
            var = found.group(1)
            libs = found.group(2)
            if var in ret:
                li = ret[var]
            else:
                li = []
            for pat in string_patterns:
                for slib in pat.finditer(libs):
                    pkg = slib.group(1)
                    li.append( Pkg(pkg, installed_version(pkg, folder)) )
            ret[var] = li
    return ret


def to_lib_dict(info, ret):
    for libs in info.values():
        for lib in libs:
            ret[lib.pkg] = lib.version


def json_file():
    home = os.path.expanduser('~')
    return os.path.join(home, '.aur_deps.json')


#############################################################################

def handle_ls(args):
    aur = aur_path()
    projects = find_git_folders(aur)
    for p in projects:
        name = get_project_name(p)
        print(name)
        print('Git:', git_info(p))
        info = pkg_info(p)
        for section, libs in info.items():
            print(section)
            for lib in libs:
                print('  ', lib.pkg, lib.version)
        print()


def handle_check(args):
    aur = aur_path()
    projects = find_git_folders(aur)
    map = None
    if os.path.isfile(json_file()):
        with open(json_file(), 'r') as f:
            map = json.loads(f.read())
    else:
        print('Note:')
        print('Missing json file, less checks will be done')
        print()
    for p in projects:
        git_fetch(p)
        print(p, git_info(p))
        if map is not None:
            info = pkg_info(p)
            differs = False
            for libs in info.values():
                for lib in libs:
                    if map[lib.pkg] != lib.version:
                        print('  ', lib.pkg, ' differs')
                        differs = True
            if differs:
                print()


def handle_write(args):
    aur = aur_path()
    projects = find_git_folders(aur)
    map = {}
    for p in projects:
        name = get_project_name(p)
        print(name)
        to_lib_dict(pkg_info(p), map)
    print('Writing json to {}'.format(json_file()))
    with open(json_file(), 'w') as f:
        f.write(json.dumps(map, sort_keys=True, indent=4))
    print('done.')
    print()


def main():
    parser = argparse.ArgumentParser(description='aur helper tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('ls', help='list aur libraries')
    sub.set_defaults(func=handle_ls)

    sub = sub_parsers.add_parser('check', help='check aur libraries for updates')
    sub.set_defaults(func=handle_check)

    sub = sub_parsers.add_parser('write', help='write current dependency status to json')
    sub.set_defaults(func=handle_write)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

