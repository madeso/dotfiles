#!/usr/bin/env python3

########################################################################################################################
# Imports

import argparse
import os
import filecmp
import subprocess
import shutil
import sys
import platform

########################################################################################################################
# Configs

interesting_files = [('_vimrc', '.vimrc')]
interesting_directories = [('vimfiles', '.vim')]


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
    if dry_run:
        if not verbose:
            print('Removing file', file_to_remove)
    else:
        os.remove(file_to_remove)


def list_files(folder):
    paths = []
    for root, dirs, files in os.walk(folder):
        for filename in files:
            full_name = os.path.join(root, filename)
            relative_path = os.path.relpath(full_name, folder)
            paths.append(relative_path)
    return paths


def replace_with(l, src, dst):
    r = []
    for s in l:
        if s.startswith(src):
            s = dst + s[len(src):]
        r.append(s)
    return r

def list_files_in_both(folder, verbose):
    if verbose:
        print("Checking", folder)
    absolute_home = os.path.join(home_folder, folder[1])
    absolute_source = os.path.join(source_folder, folder[0])
    relative_files_in_source = list_files(absolute_source)
    relative_files_in_home = list_files(absolute_home)
    relative_files_in_home_as_source = replace_with(relative_files_in_home, folder[1], folder[0])

    all_files = relative_files_in_home_as_source + relative_files_in_source
    unique_source = list(set(all_files))
    unique_dest = replace_with(unique_source, folder[0], folder[1])
    zipped = zip(unique_source, unique_dest)
    return zipped


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
        p = os.path.join(src, file[1])
        if file_exist(p):
            if verbose:
                print("File exists ", p)
            remove_file(p, verbose, dry)
        else:
            if verbose:
                print("File doesn't exists ", p)
    for src_dir, local_dir in interesting_directories:
        p = os.path.join(src, local_dir)
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
            if dry:
                print("Removing ", dst)
            else:
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
    print('Copying file', src, "to", dst)
    if not dry:
        dir = os.path.dirname(os.path.abspath(dst))
        if not os.path.exists(dir):
            print("Needed to create directory:", dir)
            os.makedirs(dir)
        shutil.copy(src, dst)


def copy_command(src, dst, args, src_index, dst_index):
    if args.remove:
        clean_interesting(dst, args.verbose, args.dry)
    for file in interesting_files:
        src_path = os.path.join(src, file[src_index])
        dst_path = os.path.join(dst, file[dst_index])
        file_copy(src_path, dst_path, args.remove, args.force, args.verbose, args.ignore_errors, args.dry)
    for dir in interesting_directories:
        for root, dirs, files in os.walk(os.path.join(src, dir[src_index]), topdown=False):
            for file in files:
                src_path = os.path.join(root, file)
                relative_path = os.path.relpath(src_path, src)
                dst_path = os.path.join(dst, relative_path.replace(dir[src_index], dir[dst_index]))
                file_copy(src_path, dst_path, args.remove, args.force, args.verbose, args.ignore_errors, args.dry)


def add_remove_commands(sub):
    add_verbose(sub)
    add_dry(sub)


def remove_command(src, args):
    clean_interesting(src, args.verbose, args.dry)


def file_info(relative_file, verbose):
    absolute_home = os.path.join(home_folder, relative_file[1])
    absolute_source = os.path.join(source_folder, relative_file[0])
    if verbose:
        print('Checking', relative_file)
    if not file_exist(absolute_home):
        print("Missing in HOME", absolute_home)
        return
    if not file_exist(absolute_source):
        print("Missing in SRC", absolute_source)
        return
    if not file_same(absolute_home, absolute_source):
        print("Different", absolute_home, absolute_source)
        return
    if verbose:
        print("Same", absolute_home, absolute_source)


def dir_info(folder, verbose):
    files = list_files_in_both(folder, verbose)
    for file in files:
        file_info(file, verbose)


########################################################################################################################
# Command functions

def handle_install(args):
    copy_command(source_folder, home_folder, args, 0, 1)


def handle_uninstall(args):
    remove_command(home_folder, args)


def handle_update(args):
    copy_command(home_folder, source_folder, args, 1, 0)


def handle_status(args):
    print('HOME: ', home_folder)
    print('SRC: ', source_folder)
    print()
    for file in interesting_files:
        file_info(file, args.verbose)

    for directory in interesting_directories:
        dir_info(directory, args.verbose)


def handle_home(args):
    s = platform.system()
    if s == 'Windows':
        subprocess.call(['explorer', home_folder])
    elif s == 'Linux':
        subprocess.call(['nautilus', home_folder])
    elif s == 'Os X':
        subprocess.call(['dont know', home_folder])
    else:
        print("Unknown OS", s)


def call_diff_app(left, right):
    s = platform.system()
    if s == 'Windows':
        subprocess.call(['WinMergeU.exe', '/e', '/x', '/u', '/maximize', left, right])
    elif s == 'Linux':
        subprocess.call(['dont know'])
    elif s == 'Os X':
        subprocess.call(['dont know'])
    else:
        print("Unknown OS", s)


def diff_single_file(relative_file):
    absolute_home = os.path.join(home_folder, relative_file[1])
    absolute_source = os.path.join(source_folder, relative_file[0])
    call_diff_app(absolute_home, absolute_source)

def handle_diff(args):
    if args.file is not None:
        for file in interesting_files:
            if file[0] == args.file or file[1] == args.file:
                diff_single_file(file)

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

    sub = sub_parsers.add_parser('grab', aliases=['get'], help='Copy files from HOME to git')
    add_copy_commands(sub)
    sub.set_defaults(func=handle_update)

    diff = sub_parsers.add_parser('diff', help='Diff files and stuff')
    diff.add_argument('--file', help='File to diff')
    diff.set_defaults(func=handle_diff)

    sub = sub_parsers.add_parser('status', aliases=['stat'], help='List the current status')
    add_verbose(sub)
    sub.set_defaults(func=handle_status)

    sub = sub_parsers.add_parser('home', help='Start explorer in home')
    sub.set_defaults(func=handle_home)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
        print('Done!')
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
