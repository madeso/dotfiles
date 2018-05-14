#!/usr/bin/env python3

import argparse
import os
import filecmp
import subprocess
import shutil
import sys
import platform
import typing


def get_home_folder() -> str:
    return os.path.expanduser('~')


def get_src_folder() -> str:
    return os.path.dirname(os.path.abspath(__file__))


class VarPath:
    def __init__(self, base: typing.Optional[str], path: str, subdir: typing.Optional[str]):
        if base is None:
            if subdir is None:
                self.path = path
            else:
                self.path = os.path.join(subdir, path)
        else:
            if subdir is None:
                self.path = os.path.join(base, path)
            else:
                self.path = os.path.join(base, subdir, path)

    def get_abs_path(self) -> str:
        return os.path.join(get_home_folder(), self.path)


class Path:
    def __init__(self, src: str, home: VarPath):
        self.home = home
        self.src = src


class Dir:
    def __init__(self, src: str, home: str):
        self.files = []
        self.home = home
        self.src = src
        self.subdir = None

    def set_dir(self, subdir: str) -> 'Dir':
        self.subdir = subdir
        return self

    def file(self, path: str) -> 'Dir':
        if self.subdir is None:
            self.files.append(Path(
                os.path.join(self.src, path),
                VarPath(self.home, path, None)
            ))
        else:
            self.files.append(Path(
                os.path.join(self.src, self.subdir, path),
                VarPath(self.home, path, self.subdir)
            ))
        return self


class Data:
    def __init__(self, interesting_files: typing.List[Path]):
        self.interesting_files = interesting_files

    def add_dir(self, subdir: Dir):
        for f in subdir.files:
            self.interesting_files.append(f)


def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def file_same(lhs: str, rhs: str) -> bool:
    if file_exist(lhs) and file_exist(rhs):
        return filecmp.cmp(lhs, rhs)
    else:
        return False


def remove_file(file_to_remove: str, verbose: bool, dry_run: bool):
    if verbose:
        print('Removing file', file_to_remove)
    if dry_run:
        if not verbose:
            print('Removing file', file_to_remove)
    else:
        os.remove(file_to_remove)


def error_detected(ignore_errors: bool):
    if not ignore_errors:
        print('Halting program because an error was detected')
        sys.exit(-42)


def clean_interesting(use_home: bool, verbose: bool, dry: bool, data: Data):
    for file in data.interesting_files:
        p = file.home.get_abs_path() if use_home else os.path.join(get_src_folder(), file.src)
        if file_exist(p):
            if verbose:
                print("File exists ", p)
            remove_file(p, verbose, dry)
        else:
            if verbose:
                print("File doesn't exists ", p)


def add_verbose(sub):
    sub.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='Verbose output')


def add_dry(sub):
    sub.add_argument('--dry-run', '--dry', '-0', dest='dry', action='store_true', help="Don't copy or remove anything")


def add_copy_commands(sub):
    add_verbose(sub)
    add_dry(sub)
    sub.add_argument('--remove', '-r', dest='remove', action='store_true', help='Remove destination before copying')
    sub.add_argument('--force', '-f', dest='force', action='store_true', help='Force copy even if the file exist')
    sub.add_argument('--ignore-errors', '--continue-on-error', dest='ignore_errors', action='store_true',
                     help="Don't stop on errors")


def file_copy(src: str, dst: str, remove: bool, force: bool, verbose: bool, ignore_errors: bool, dry: bool):
    if not file_exist(src):
        print('Missing file', src)
        error_detected(ignore_errors)
    if file_exist(dst):
        if remove:
            if dry:
                print("Removing ", dst)
            else:
                remove_file(dst, verbose, False)
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
        subdir = os.path.dirname(os.path.abspath(dst))
        if not os.path.exists(subdir):
            print("Needed to create directory:", subdir)
            os.makedirs(subdir)
        shutil.copy(src, dst)


def copy_command(args, data: Data, install: bool):
    if args.remove:
        clean_interesting(install, args.verbose, args.dry, data)
    for file in data.interesting_files:
        home_path = file.home.get_abs_path()
        src_path = os.path.join(get_src_folder(), file.src)
        from_path = src_path if install else home_path
        to_path = home_path if install else src_path
        file_copy(from_path, to_path, args.remove, args.force, args.verbose, args.ignore_errors, args.dry)


def add_remove_commands(sub):
    add_verbose(sub)
    add_dry(sub)


def remove_command(use_home: bool, args, data: Data):
    clean_interesting(use_home, args.verbose, args.dry, data)


def file_info(relative_file: Path, verbose: bool):
    absolute_home = relative_file.home.get_abs_path()
    absolute_source = os.path.join(get_src_folder(), relative_file.src)
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


def call_diff_app(left: str, right: str):
    s = platform.system()
    if s == 'Windows':
        subprocess.call(['WinMergeU.exe', '/e', '/x', '/u', '/maximize', left, right])
    elif s == 'Linux':
        subprocess.call(['unknown'])
    elif s == 'Os X':
        subprocess.call(['unknown'])
    else:
        print("Unknown OS", s)


def diff_single_file(relative_file: Path):
    absolute_home = relative_file.home.get_abs_path()
    absolute_source = os.path.join(get_src_folder(), relative_file.src)
    call_diff_app(absolute_home, absolute_source)


########################################################################################################################
# Command functions

def handle_install(args, data: Data):
    copy_command(args, data, True)


def handle_uninstall(args, data: Data):
    remove_command(True, args, data)


def handle_update(args, data: Data):
    copy_command(args, data, False)


def handle_status(args, data: Data):
    print('HOME: ', get_home_folder())
    print('SRC: ', get_src_folder())
    print()
    for file in data.interesting_files:
        file_info(file, args.verbose)


def handle_home(args, data: Data):
    s = platform.system()
    if s == 'Windows':
        subprocess.call(['explorer', get_home_folder()])
    elif s == 'Linux':
        subprocess.call(['nautilus', get_home_folder()])
    elif s == 'Os X':
        subprocess.call(['unknown', get_home_folder()])
    else:
        print("Unknown OS", s)


def handle_diff(args, data: Data):
    if args.file is not None:
        for file in data.interesting_files:
            if file.src == args.file or file.home == args.file:
                diff_single_file(file)


########################################################################################################################
# Main

def main(data: Data):
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
        args.func(args, data)
        print('Done!')
    else:
        parser.print_help()
