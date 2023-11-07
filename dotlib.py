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
import time
import collections
from enum import Enum

from external.prettygood.config import *

# removed
# generate_file
# file_generate
# generate_file_as_str
# GeneratedFile
# generated_same
# GenerationData

# to be removed

SETTINGS_CLASS = Settings('class', [])


def get_config() -> Config:
    return get_user_data('dotlib')


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
    if has_class('wsl'):
        user = subprocess.check_output(['cmd.exe', '/c', 'echo', '%username%'], text=True).strip()
        print(user)
        appdata = '/mnt/c/Users/{}/Appdata/Roaming'.format(user)
        return appdata
    return os.getenv('APPDATA')


def get_src_folder() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def is_windows() -> bool:
    return has_class('wsl') or platform.system() == 'Windows'


def is_osx() -> bool:
    return platform.system() == 'Darwin'


class PathType(Enum):
    USER = 1
    APPDATA_ROAMING = 2
    APPDATA_LOCAL = 3


def get_folder(path: PathType) -> str:
    if path == PathType.APPDATA_ROAMING:
        return get_appdata_roaming_folder()
    elif path == PathType.APPDATA_LOCAL:
        roaming = get_appdata_roaming_folder()
        return os.path.normpath(os.path.join(roaming, '..', 'Local'))
    return get_home_folder()


def is_running(app: str) -> bool:
    try:
        import psutil
        return app in (p.name() for p in psutil.process_iter())
    except ModuleNotFoundError:
        print('psutil not found, try pip install psutil')
        return False


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
    def __init__(self, classes: typing.List[str], src: str, home: VarPath):
        self.classes = classes
        self.home = home
        self.src = src


class Dir:
    def __init__(self, classes: typing.List[str], src: str, home: str, win_where: PathType = PathType.USER, win_home: typing.Optional[str]=None, osx_home: typing.Optional[str]=None):
        self.classes = classes
        self.files = []
        self.home = home
        if is_windows() and win_home is not None:
            self.home = win_home
        if is_osx() and osx_home is not None:
            self.home = osx_home
        self.src = src
        self.subdir = None
        self.win_where = win_where

    def set_dir(self, subdir: str) -> 'Dir':
        self.subdir = subdir
        return self

    def add_dir(self, subdir: str) -> 'Dir':
        self.add_dir_rec(subdir)
        return self

    def add_dir_rec(self, subdir: str):
        p = os.path.join(get_src_folder(), self.src, subdir)
        # work in progress...
        # todo: traverse all files in subdir and add them to self.files
        for entry in os.listdir(p):
            if entry == '.git':
                pass
            else:
                if os.path.isfile(os.path.join(get_src_folder(), self.src, subdir, entry)):
                    self.files.append(Path(self.classes,
                        os.path.join(self.src, subdir, entry),
                        VarPath(self.home, entry, subdir, self.win_where)
                    ))
                else:
                    self.add_dir_rec(os.path.join(subdir, entry))

    def file(self, path: str) -> 'Dir':
        if self.subdir is None:
            self.files.append(Path(self.classes,
                os.path.join(self.src, path),
                VarPath(self.home, path, None, self.win_where)
            ))
        else:
            self.files.append(Path(self.classes,
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

    def add_file(self, classes: typing.List[str], src: str, home: str):
        file = Path(classes, src, VarPath(None, home, None, PathType.USER))
        self.interesting_files.append(file)

    def add_file_path(self, classes: typing.List[str], src: str, home: str, path: PathType):
        file = Path(classes, src, VarPath(None, home, None, path))
        self.interesting_files.append(file)

    def add_dir(self, subdir: Dir):
        for f in subdir.files:
            self.interesting_files.append(f)


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


def add_verbose(sub):
    sub.add_argument('--verbose', '-v', dest='verbose', action='store_true', help='Verbose output')


def add_dry(sub):
    sub.add_argument('--dry-run', '--dry', '-0', dest='dry', action='store_true', help="Don't copy or remove anything")


def add_copy_commands(sub):
    sub.add_argument('search', nargs='*')
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



# https://stackoverflow.com/a/49007649/180307
class Watcher(object):
    refresh_delay_secs = 1

    # Constructor
    def __init__(self, watch_files, call_func_on_change=None):
        self.filenames = watch_files
        self.call_func_on_change = call_func_on_change
        self._cached_stamps = [os.stat(f).st_mtime for f in self.filenames]

    # Look for changes
    def look(self):
        file_changed = False

        for i in range(len(self.filenames)):
            stamp = os.stat(self.filenames[i]).st_mtime
            if stamp != self._cached_stamps[i]:
                self._cached_stamps[i] = stamp
                file_changed = True
                print('{} changed'.format(self.filenames[i]))

        if file_changed:
            print('Change detected...')
            if self.call_func_on_change is not None:
                self.call_func_on_change()

    # Keep watching in a loop        
    def watch(self):
        while True: 
            try: 
                time.sleep(self.refresh_delay_secs) 
                self.look() 
            except KeyboardInterrupt: 
                print('\nDone') 
                break 
            except FileNotFoundError:
                pass


def matchlist_contains_file(terms: typing.List[str], path: str) -> bool:
    if len(terms) == 0:
        return True
    for t in terms:
        if t not in path:
            return False
    return True


def has_atleast_one_class(classes: typing.List[str]) -> bool:
    for c in classes:
        if has_class(c):
            return True
    return False


def for_each_file(data: Data, install: bool, verb: str, search: typing.List[str], callback_copy):
    total = 0
    operated = 0
    
    for file in data.interesting_files:
        if has_atleast_one_class(file.classes):
            total += 1
            home_path = file.home.get_abs_path()
            src_path = os.path.join(get_src_folder(), file.src)
            from_path = src_path if install else home_path
            to_path = home_path if install else src_path
            if matchlist_contains_file(search, from_path) or matchlist_contains_file(search, to_path):
                operated += 1
                callback_copy(from_path, to_path)
    print('{} of {} {}.'.format(operated, total, verb))


def run_copy_command(args, data: Data, install: bool):
    if args.remove:
        clean_interesting(install, args.verbose, args.dry, data)
    for_each_file(data, install, verb='copied', search=args.search,
                  callback_copy=lambda from_path, to_path: file_copy(from_path, to_path, args.remove,
                                                                     args.force, args.verbose, args.ignore_errors,
                                                                     args.dry)
                  )

    if is_running('termite'):
        print('Refreshing termite')
        subprocess.run(['killall', '-USR1', 'termite'])


def copy_command(args, data: Data, install: bool):
    run_copy_command(args, data, install)


def run_print_command(args, data: Data):
    def print_copied(from_path, to_path):
        print('Copying {} -> {}'.format(from_path, to_path))
        print()

    for_each_file(data, True, verb='printed', search=args.search, callback_copy=print_copied)


def add_remove_commands(sub):
    add_verbose(sub)
    add_dry(sub)


def remove_command(use_home: bool, args, data: Data):
    clean_interesting(use_home, args.verbose, args.dry, data)


def print_file_infos(data: Data, verbose: bool):
    def file_diff(absolute_home: str, absolute_source: str, diff_callback):
        if verbose:
            print()
            print('Checking', absolute_home)
        if not file_exist(absolute_home):
            print("Missing in HOME", absolute_home)
            return
        if not file_exist(absolute_source):
            print("Missing in SRC", absolute_source)
            return
        if not diff_callback(absolute_home, absolute_source):
            print("Different", absolute_home, absolute_source)
            return
        if verbose:
            print("Same", absolute_home, absolute_source)

    for_each_file(data, True, 'status printed', search=[],
                  callback_copy=lambda source, home: file_diff(home, source, file_same))


def call_diff_app(left: str, right: str):
    s = platform.system()
    if s == 'Windows':
        winmerge = find_path('WinMergeU.exe', get_default_search_paths(), 'WinMerge')
        if winmerge is None:
            print('Unable to find WinMerge')
        else:
            subprocess.call([winmerge, '/e', '/x', '/u', '/maximize', left, right])
    elif s == 'Linux':
        try:
            subprocess.call(['meld', left, right])
        except OSError as e:
            import errno
            if e.errno == errno.ENOENT:
                print("Note: Meld isn't installed")
                subprocess.call(['diff', left, right, '--color'])
                # print(diff)
            else:
                raise
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


########################################################################################################################
# Command functions

def handle_install(args, data: Data):
    copy_command(args, data, True)


def handle_watch(args, data: Data):
    # todo(Gustav): make sure this works...
    files = [os.path.join(get_src_folder(), f.src) for f in data.files]

    def on_action():
        print()
        copy_command(args, data, True)
        print()

    watcher = Watcher(files, on_action)
    watcher.watch()


def handle_print(args, data: Data):
    run_print_command(args, data)


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
    print_file_infos(data, args.verbose)


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


def handle_class(args, data: Data):
    c = collections.Counter()
    for f in data.interesting_files:
        c = c + collections.Counter(f.classes)
    existing_classes = frozenset(name for name, count in c.items())

    config = get_config()

    classes = SETTINGS_CLASS.get_value(config)

    if args.value:
        if not args.remove and args.value not in classes:
            classes.append(args.value)
        if args.remove and args.value in classes:
            classes.remove(args.value)
        SETTINGS_CLASS.set_value(config, classes)
        config.save()

    if len(classes) > 0:
        print('Classes:')
        for c in classes:
            x = '*' if c in existing_classes else ' '
            print(' ' + x + c)

    classes_to_add = list(c for c in existing_classes if c not in classes)
    if len(classes_to_add) > 0:
        print()
        print('Classes to add:')
        for c in classes_to_add:
            print('  ' + c)


def has_class(c: str) -> bool:
    config = get_config()
    values = SETTINGS_CLASS.get_value(config)
    return c in values


def handle_diff(args, data: Data):
    matches = []
    for_each_file(data, True, 'diff matches', args.file,
                  callback_copy=lambda from_path, to_path: matches.append((from_path, to_path)))
    matches = list(set(matches))
    if len(matches) == 1:
        src, home = matches[0]
        call_diff_app(src, home)
    else:
        if args.print:
            for m in matches:
                src, home, generate = m
                print("Generated" if generate else "Copied")
                print('Source:', src)
                print('Home:  ', home)
                print('')


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

    sub = sub_parsers.add_parser('watch', help='watch files for changes and install them')
    add_copy_commands(sub)
    sub.set_defaults(func=handle_watch)

    sub = sub_parsers.add_parser('grab', aliases=['get'], help='Copy files from HOME to git')
    add_copy_commands(sub)
    sub.set_defaults(func=handle_update)

    diff = sub_parsers.add_parser('diff', help='Diff files and stuff')
    diff.add_argument('file', nargs='+', help='File pattern to diff')
    diff.add_argument('-p', '--print', action='store_true', help='Print matches if no exact match was found.')
    diff.set_defaults(func=handle_diff)

    sub = sub_parsers.add_parser('print', aliases=['debug'], help='Print generated files')
    sub.add_argument('search', nargs='*', help='selections of file patterns to debug')
    sub.set_defaults(func=handle_print)

    sub = sub_parsers.add_parser('status', aliases=['stat'], help='List the current status')
    add_verbose(sub)
    sub.set_defaults(func=handle_status)

    sub = sub_parsers.add_parser('home', help='Start explorer in home')
    sub.set_defaults(func=handle_home)

    sub = sub_parsers.add_parser('class', help='Get or set the class')
    sub.add_argument('value', nargs='?', help='if specified, add this class')
    sub.add_argument('--remove', action='store_true', help='remove class instead of adding it')
    sub.set_defaults(func=handle_class)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args, data)
        print('Done!')
    else:
        parser.print_help()
