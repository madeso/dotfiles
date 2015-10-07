#!/usr/bin/env python3

########################################################################################################################
# Imports

import argparse
import os
import filecmp
import subprocess


########################################################################################################################
# Configs

interesting_files = ['_vimrc']
interesting_directories = ['vimfiles']

########################################################################################################################
# Globals

home = os.path.expanduser('~')
root = os.path.dirname(os.path.abspath(__file__))

########################################################################################################################
# Util functions

def file_exist(file):
    return os.path.isfile(file)


def file_same(lhs, rhs):
    return filecmp.cmp(lhs, rhs)


def list_files(folder):
    ret = []
    for root, dirs, files in os.walk(folder):
        for name in files:
            fullname = os.path.join(root, name)
            relative = os.path.relpath(fullname, folder)
            ret.append(relative)
    return ret


def list_files_in_both(folder):
    h = os.path.join(home, folder)
    s = os.path.join(root, folder)
    c = list_files(h) + list_files(s)
    return list(set(c))


########################################################################################################################
# Command helpers

def remove_and_copy(src, dst, should_remove, should_copy):
    pass


def file_info(path, verbose):
    h = os.path.join(home, path)
    s = os.path.join(root, path)
    if verbose:
        print('Checking', path)
    if not file_exist(h):
        print("Missing HOME", h)
        return
    if not file_exist(s):
        print("Missing SRC", s)
        return
    if not file_same(h, s):
        print("Different ", h, s)
        return


def dir_info(folder, verbose):
    files = list_files_in_both(folder)
    for file in files:
        file_info(os.path.join(folder, file), verbose)

########################################################################################################################
# Command functions

def handle_install(args):
    print("Install")


def handle_uninstall(args):
    print("Uninstall")


def handle_update(args):
    print("Update")


def handle_status(args):
    print('HOME: ', home)
    print('SRC: ', root)
    print()
    for file in interesting_files:
        file_info(file, args.verbose)

    for ddir in interesting_directories:
        dir_info(ddir, args.verbose)


def handle_home(args):
    subprocess.call(['explorer', home])


def main():
    parser = argparse.ArgumentParser(description='Manage my dot files.')
    parsers = parser.add_subparsers(help='sub-command help')

    sub = parsers.add_parser('install', aliases=['copy', 'in', 'co'], help='copy files to HOME')
    sub.set_defaults(func=handle_install)

    sub = parsers.add_parser('uninstall', aliases=['remove', 're', 'un'], help='remove files from HOME')
    sub.set_defaults(func=handle_uninstall)

    sub = parsers.add_parser('update', aliases=['up'], help='copy files from HOME to git')
    sub.set_defaults(func=handle_update)

    sub = parsers.add_parser('status', aliases=['stat'], help='list the current status')
    sub.add_argument('--verbose', action='store_true', help='Verbose printing')
    sub.set_defaults(func=handle_status)

    sub = parsers.add_parser('home', aliases=['stat'], help='start explorer in home')
    sub.set_defaults(func=handle_home)


    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
