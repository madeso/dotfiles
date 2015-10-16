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

home_folder = os.path.expanduser('~')
source_folder = os.path.dirname(os.path.abspath(__file__))


########################################################################################################################
# Util functions

def file_exist(file):
    return os.path.isfile(file)


def file_same(lhs, rhs):
    return filecmp.cmp(lhs, rhs)


def remove_file(file_to_remove, verbose, dry_run):
    if verbose:
        print('Removing file', file_to_remove)
    if not dry_run:
        os.remove(file_to_remove)


def list_files(folder):
    paths = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            full_name = os.path.join(root, filename)
            relative_path = os.path.relpath(full_name, folder)
            paths.append(relative_path)
    return paths


def list_files_in_both(folder):
    absolute_home = os.path.join(home_folder, folder)
    absolute_source = os.path.join(source_folder, folder)
    all_files = list_files(absolute_home) + list_files(absolute_source)
    unique_files = list(set(all_files))
    return unique_files


def remove_files(folder, verbose, dry):
    for root, dirs, files in os.walk(folder, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            remove_file(file_path, verbose, dry)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if verbose:
                print('Removing directory ', dir_path)
            if not dry:
                os.rmdir(dir_path)
    if verbose:
        print('Removing directory ', folder)
    if not dry:
        os.rmdir(os.path.join(folder))


def error_detected(ignore_errors):
    if not ignore_errors:
        print('Halting program because an error was detected')
        sys.exit(-42)

########################################################################################################################
# Command helpers

def clean_interesting(src, verbose, dry):
    for file in interesting_files:
        p = os.path.join(src, file)
        if file_exist(p):
            remove_file(p, verbose, dry)
    for dir in interesting_directories:
        p = os.path.join(src, dir)
        remove_files(p, verbose, dry)


def add_verbose(sub):
    sub.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='Verbose output')


def add_dry(sub):
    sub.add_argument('--dry-run', '--dry', '-0', dest='dry', action='store_true', help="Don't copy or remove anything")


def add_copy_commands(sub):
    add_verbose(sub)
    add_dry(sub)
    sub.add_argument('--remove', '-r', dest='remove', action='store_true', help='Remove destination before copying')
    sub.add_argument('--force', '-f', dest='force', action='store_true', help='Force copy even if the file exist')
    sub.add_argument('--ignore-errors', '--continue-on-error', dest='ignore_errors', action='store_true', help="Don't stop on errors")


def file_copy(src, dst, remove, force, verbose, ignore_errors, dry):
    if not file_exist(src):
        print('Missing file', src)
        error_detected(ignore_errors)
    if file_exist(dst):
        if remove:
            remove_file(dst, verbose, dry)
        else:
            if file_same(src, dst):
                if verbose:
                    print('Files are the same', src, dst)
                if not force:
                    if verbose:
                        print('File exist, ignoring (use force)', dst)
                    return
            else:
                if verbose:
                    print('Files are not the same', src, dst)
    print('Copying file', src, dst)
    if not dry:
        shutil.copy(src, dst)


def copy_command(src, dst, args):
    if args.remove:
        clean_interesting(dst, args.verbose, args.dry)
    for file in interesting_files:
        src_path = os.path.join(src, file)
        dst_path = os.path.join(dst, file)
        file_copy(src_path, dst_path, args.remove, args.force, args.verbose, args.ignore_errors, args.dry)
    for directory in interesting_directories:
        for root, dirs, files in os.walk(os.path.join(src, directory), topdown=False):
            for file in files:
                src_path = os.path.join(root, file)
                relative_path = os.path.relpath(src_path, src)
                dst_path = os.path.join(dst, relative_path)
                file_copy(src_path, dst_path, args.remove, args.force, args.verbose, args.ignore_errors, args.dry)


def add_remove_commands(sub):
    add_verbose(sub)
    add_dry(sub)


def remove_command(src, args):
    clean_interesting(src, args.verbose, args.dry)


def file_info(relative_file, verbose):
    absolute_home = os.path.join(home_folder, relative_file)
    absolute_source = os.path.join(source_folder, relative_file)
    if verbose:
        print('Checking', relative_file)
    if not file_exist(absolute_home):
        print("Missing in HOME", absolute_home)
        return
    if not file_exist(absolute_source):
        print("Missing in SRC", absolute_source)
        return
    if not file_same(absolute_home, absolute_source):
        print("Different ", absolute_home, absolute_source)
        return


def dir_info(folder, verbose):
    files = list_files_in_both(folder)
    for file in files:
        file_info(os.path.join(folder, file), verbose)


########################################################################################################################
# Command functions

def handle_install(args):
    copy_command(source_folder, home_folder, args)


def handle_uninstall(args):
    remove_command(home_folder, args)


def handle_update(args):
    copy_command(home_folder, source_folder, args)


def handle_status(args):
    print('HOME: ', home_folder)
    print('SRC: ', source_folder)
    print()
    for file in interesting_files:
        file_info(file, args.verbose)

    for directory in interesting_directories:
        dir_info(directory, args.verbose)


def handle_home(args):
    subprocess.call(['explorer', home_folder])


########################################################################################################################
# Main

def main():
    parser = argparse.ArgumentParser(description='Manage my dot files.')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('install', aliases=['copy', 'in', 'co'], help='Copy files to HOME')
    add_copy_commands(sub)
    sub.set_defaults(func=handle_install)

    sub = sub_parsers.add_parser('uninstall', aliases=['remove', 're', 'un'], help='Remove files from HOME')
    add_remove_commands(sub)
    sub.set_defaults(func=handle_uninstall)

    sub = sub_parsers.add_parser('update', aliases=['up'], help='Copy files from HOME to git')
    add_copy_commands(sub)
    sub.set_defaults(func=handle_update)

    sub = sub_parsers.add_parser('status', aliases=['stat'], help='List the current status')
    add_verbose(sub)
    sub.set_defaults(func=handle_status)

    sub = sub_parsers.add_parser('home', help='Start explorer in home')
    sub.set_defaults(func=handle_home)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
        print('Done')
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
