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


def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def get_default_search_paths() -> typing.List[str]:
    if is_windows():
        return ['C:\\Program Files (x86)',
                'C:\\Program Files']
    else:
        return []


def find_path(file: str, paths: typing.List[str], folder: str) -> typing.Optional[str]:
    for subdir in paths:
        p = os.path.join(subdir, folder, file)
        if file_exist(p):
            return p
    return None


def get_home_folder() -> str:
    return os.path.expanduser('~')


def get_appdata_roaming_folder() -> str:
    return os.getenv('APPDATA')


def get_src_folder() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def is_windows() -> bool:
    return platform.system() == 'Windows'


class PathType(Enum):
    USER = 1
    APPDATA_ROAMING = 2


def get_folder(path: PathType) -> str:
    if path == PathType.APPDATA_ROAMING:
        return get_appdata_roaming_folder()
    return get_home_folder()


def get_config_file_name() -> str:
    return os.path.join(get_home_folder(), '.dotlib.json')


def get_user_data() -> typing.Dict[str, str]:
    if file_exist(get_config_file_name()):
        with open(get_config_file_name(), 'r') as f:
            return json.loads(f.read())
    else:
        return {}


def set_user_data(data: typing.Dict[str, str]):
    with open(get_config_file_name(), 'w') as f:
        print(json.dumps(data, sort_keys=True, indent=4), file=f)


def get_computer_name() -> str:
    data = get_user_data()
    if 'name' in data:
        return data['name']
    else:
        return ''


def set_computer_name(name: str):
    data = get_user_data()
    data['name'] = name
    set_user_data(data)


class VarPath:
    def __init__(self, base: typing.Optional[str], path: str, subdir: typing.Optional[str], win_where: PathType):
        self.win_where = win_where
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
        base_path = get_folder(self.win_where) if is_windows() else get_home_folder()
        return os.path.join(base_path, self.path)


class Path:
    def __init__(self, src: str, home: VarPath):
        self.home = home
        self.src = src


class Dir:
    def __init__(self, src: str, home: str, win_where: PathType = PathType.USER, win_home: typing.Optional[str]=None):
        self.files = []
        self.home = win_home if is_windows() and win_home is not None else home
        self.src = src
        self.subdir = None
        self.win_where = win_where

    def set_dir(self, subdir: str) -> 'Dir':
        self.subdir = subdir
        return self

    def file(self, path: str) -> 'Dir':
        if self.subdir is None:
            self.files.append(Path(
                os.path.join(self.src, path),
                VarPath(self.home, path, None, self.win_where)
            ))
        else:
            self.files.append(Path(
                os.path.join(self.src, self.subdir, path),
                VarPath(self.home, path, self.subdir, self.win_where)
            ))
        return self


class Data:
    @staticmethod
    def _empty_files() -> typing.List[Path]:
        return []

    def __init__(self):
        self.interesting_files = Data._empty_files()
        self.generated_files = Data._empty_files()
        self.vars = GenerationData()

    def set_vars(self, **kwargs):
        for key, value in kwargs.items():
            self.vars.set(key, value)

    def set_var_alias(self, **kwargs):
        for key, value in kwargs.items():
            self.vars.set_alias(key, value)

    def add_file(self, src: str, home: str):
        file = Path(src, VarPath(None, home, None, PathType.USER))
        self.interesting_files.append(file)

    def add_generated_file(self, src: str, home: str):
        file = Path(src, VarPath(None, home, None, PathType.USER))
        self.generated_files.append(file)

    def add_dir(self, subdir: Dir):
        for f in subdir.files:
            self.interesting_files.append(f)


class GenerationData:
    @staticmethod
    def _empty_dictionary() -> typing.Dict[str, str]:
        return {}

    def __init__(self):
        self.data = GenerationData._empty_dictionary()
        self.alias = GenerationData._empty_dictionary()

    def set_alias(self, name: str, val: str):
        self.alias[name] = val

    def set_raw(self, name: str, val: str):
        self.data[name] = val
        if val[0] == '#':
            # also write this as rgb
            h = val.lstrip('#')
            rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
            self.set_raw('{}_rgb'.format(name), '{r}, {g}, {b}'.format(r=rgb[0], g=rgb[1], b=rgb[2]))

    def set(self, name: str, val: str):
        self.set_raw(name, val)
        for (n, v) in self.alias.items():
            if v == name:
                self.set_raw(n, val)


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


def clean_single_file(use_home: bool, verbose: bool, dry: bool, file: Path):
    p = file.home.get_abs_path() if use_home else os.path.join(get_src_folder(), file.src)
    if file_exist(p):
        if verbose:
            print("File exists ", p)
        remove_file(p, verbose, dry)
    else:
        if verbose:
            print("File doesn't exists ", p)


def clean_interesting(use_home: bool, verbose: bool, dry: bool, data: Data):
    for file in data.interesting_files:
        clean_single_file(use_home, verbose, dry, file)
    if use_home:
        for file in data.generated_files:
            clean_single_file(use_home, verbose, dry, file)


def add_verbose(sub):
    sub.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='Verbose output')


def add_dry(sub):
    sub.add_argument('--dry-run', '--dry', '-0', dest='dry', action='store_true', help="Don't copy or remove anything")


def add_copy_commands(sub):
    add_verbose(sub)
    add_dry(sub)
    sub.add_argument('--remove', '-r', dest='remove', action='store_true', help='Remove destination before copying')
    sub.add_argument('--force', '-f', dest='force', action='store_true', help='Force copy even if the file exist')
    sub.add_argument('--ignore-errors', '--continue-on-error', '-ie', '-ce', dest='ignore_errors', action='store_true',
                     help="Don't stop on errors")


def file_base(src: str, dst: str, remove: bool, force: bool, verbose: bool, ignore_errors: bool, dry: bool,
              file_function):
    if not file_exist(src):
        print('Missing file', src)
        error_detected(ignore_errors)
        return
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
        file_function(src, dst)


def file_copy(src: str, dst: str, remove: bool, force: bool, verbose: bool, ignore_errors: bool, dry: bool):
    file_base(src, dst, remove, force, verbose, ignore_errors, dry, shutil.copy)


def file_generate(src: str, dst: str, remove: bool, force: bool, verbose: bool, ignore_errors: bool, dry: bool
                  , gen: GenerationData):
    file_base(src, dst, remove, force, verbose, ignore_errors, dry, lambda srcf, dstf: generate_file(srcf, dstf, gen))


def generate_file(from_path: str, to_path: str, g: GenerationData):
    import pystache
    with open(from_path, 'r') as fromf:
        with open(to_path, 'w') as tof:
            tof.write(pystache.render(fromf.read(), g.data))


def run_copy_command(args, data: Data, install: bool):
    if args.remove:
        clean_interesting(install, args.verbose, args.dry, data)
    for file in data.interesting_files:
        home_path = file.home.get_abs_path()
        src_path = os.path.join(get_src_folder(), file.src)
        from_path = src_path if install else home_path
        to_path = home_path if install else src_path
        file_copy(from_path, to_path, args.remove, args.force, args.verbose, args.ignore_errors, args.dry)
    if install:
        for file in data.generated_files:
            home_path = file.home.get_abs_path()
            src_path = os.path.join(get_src_folder(), file.src)
            from_path = src_path
            to_path = home_path
            file_generate(from_path, to_path, args.remove, args.force, args.verbose, args.ignore_errors, args.dry
                          , data.vars)

def copy_command(args, data: Data, install: bool):
  try:
    run_copy_command(args, data, install)
  except ModuleNotFoundError as err:
    print('Some parts of the copy command failed due to missing modules', file=sys.stderr)
    if 'pystache' in str(err):
      print('It looks like you are myssing pystache, "pip install pystache" should do the trick.')
    else:
      print(err, file=sys.stderr)


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
        winmerge = find_path('WinMergeU.exe', get_default_search_paths(), 'WinMerge')
        if winmerge is None:
            print('Unable to find WinMerge')
        else:
            subprocess.call([winmerge, '/e', '/x', '/u', '/maximize', left, right])
    elif s == 'Linux':
        subprocess.call(['meld', left, right])
    elif s == 'Os X':
        subprocess.call(['unknown'])
    else:
        print("Unknown OS", s)


def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


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
    if is_windows():
        print('APPDATA ROAMING: ', get_appdata_roaming_folder())
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


def handle_name(args, data: Data):
    if args.name is None:
        print(get_computer_name())
    else:
        set_computer_name(args.name)


def handle_diff(args, data: Data):
    def paths(path: Path) -> typing.List[str]:
        return [path.src, path.home.path]
    matches = []
    for file in data.interesting_files:
        for p in paths(file):
            matched = True
            for m in args.file:
                if m not in p:
                    matched = False
            if matched:
                matches.append(file)
    matches = list(set(matches))
    if len(matches) == 1:
        diff_single_file(matches[0])
    else:
        print('Found {} matches'.format(len(matches)))
        if args.print:
            for m in matches:
                for p in paths(m):
                    print(p)


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
    diff.add_argument('file', nargs='+', help='File pattern to diff')
    diff.add_argument('-p', '--print', action='store_true', help='Print matches if no exact match was found.')
    diff.set_defaults(func=handle_diff)

    sub = sub_parsers.add_parser('status', aliases=['stat'], help='List the current status')
    add_verbose(sub)
    sub.set_defaults(func=handle_status)

    sub = sub_parsers.add_parser('home', help='Start explorer in home')
    sub.set_defaults(func=handle_home)

    sub = sub_parsers.add_parser('name', help='Get or set the current computer name')
    sub.add_argument('--name', help='if specified, sets the name to this')
    sub.set_defaults(func=handle_name)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args, data)
        print('Done!')
    else:
        parser.print_help()
