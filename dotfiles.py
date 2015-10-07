#!/usr/bin/env python3

########################################################################################################################
# Imports

import argparse
import os
import filecmp
import subprocess
import shutil
import sys

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


def remove_file(p, verbose):
    if verbose:
        print('Removing file ', p)
    os.remove(p)


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


def remove_files(top, verbose):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            p = os.path.join(root, name)
            remove_file(p)
        for name in dirs:
            p = os.path.join(root, name)
            if verbose:
                print('Removing directory ', p)
            os.rmdir(os.path.join(root, name))


def error_detected(ignore_errors):
    if not ignore_errors:
        print('Halting program because an error was detected')
        sys.exit(-42)

########################################################################################################################
# Command helpers

def clean_interesting(src, verbose):
    for file in interesting_files:
        p = os.path.join(src, file)
        if file_exist(p):
            remove_file(p, verbose)
    for dir in interesting_directories:
        p = os.path.join(src, dir)
        remove_files(p, verbose)


def add_verbose(sub):
    sub.add_argument('--verbose', action='store_true', help='Verbose output')


def add_copy_commands(sub):
    add_verbose(sub)
    sub.add_argument('--remove', action='store_true', help='Remove destination before copying')
    sub.add_argument('--force', action='store_true', help='Force copy even if the file exist')
    sub.add_argument('--ignore-errors', action='store_true', help='stop on errors')


def file_copy(src, dst, remove, force, verbose, ignore_errors):
    if not file_exist(src):
        print('Missing file', src)
        error_detected(ignore_errors)
    if file_exist(dst):
        if remove:
            remove_file(dst, verbose)
        elif file_same(src, dst):
            if not force:
                if verbose:
                    print('File exist, ignoring (use force)', dst)
    if verbose:
        print('Copying file', src, dst)
    shutil.copy(src, dst)


def copy_command(src, dst, args):
    if args.remove:
        clean_interesting(dst, args.verbose)
    for file in interesting_files:
        s = os.path.join(src, file)
        d = os.path.join(dst, file)
        file_copy(s, d, args.remove, args.force, args.verbose, args.ignore_errors)
    for dir in interesting_directories:
        for root, dirs, files in os.walk(os.path.join(src, dir), topdown=False):
            for file in files:
                s = os.path.join(root, file)
                relative = os.path.relpath(s, src)
                d = os.path.join(dst, relative)
                file_copy(s, d, args.remove, args.force, args.verbose, args.ignore_errors)

def add_remove_commands(sub):
    add_verbose(sub)
    sub.add_argument('--full', action='store_true', help='Remove everything')


def remove_command(src, args):
    if args.full:
        remove_files(src, args.verbose)
    else:
        clean_interesting(src, args.verbose)


def file_info(path, verbose):
    h = os.path.join(home, path)
    s = os.path.join(root, path)
    if verbose:
        print('Checking', path)
    if not file_exist(h):
        print("Missing in HOME", h)
        return
    if not file_exist(s):
        print("Missing in SRC", s)
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
    copy_command(root, home, args)


def handle_uninstall(args):
    remove_command(home, args)


def handle_update(args):
    copy_command(home, root, args)


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


########################################################################################################################
# Main

def main():
    parser = argparse.ArgumentParser(description='Manage my dot files.')
    parsers = parser.add_subparsers(help='sub-command help')

    sub = parsers.add_parser('install', aliases=['copy', 'in', 'co'], help='copy files to HOME')
    add_copy_commands(sub)
    sub.set_defaults(func=handle_install)

    sub = parsers.add_parser('uninstall', aliases=['remove', 're', 'un'], help='remove files from HOME')
    add_remove_commands(sub)
    sub.set_defaults(func=handle_uninstall)

    sub = parsers.add_parser('update', aliases=['up'], help='copy files from HOME to git')
    add_copy_commands(sub)
    sub.set_defaults(func=handle_update)

    sub = parsers.add_parser('status', aliases=['stat'], help='list the current status')
    add_verbose(sub)
    sub.set_defaults(func=handle_status)

    sub = parsers.add_parser('home', aliases=['stat'], help='start explorer in home')
    sub.set_defaults(func=handle_home)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
