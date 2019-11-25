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


def get_src_folder() -> str:
    return os.path.dirname(os.path.abspath(__file__))


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


def run_git_update(p):
    subprocess.run(['git', 'pull'], cwd=p)


def install_pkg(p):
    #Sync, Install, Clean temporary files
    subprocess.run(['makepkg', '-sic'], cwd=p, check=True)


def clear_pkg(p):
    # todo: remove all file and folders except .git
    print('clearing ', p)
    for e in os.listdir(p):
        path = os.path.join(p, e)
        if os.path.isdir(path):
            if e != '.git':
                print('removing directory ', e)
                shutil.rmtree(path)
        else:
            os.remove(path)
    subprocess.run(['git', 'checkout', '.'], cwd=p, check=True)


def cmd(cmd, cwd):
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT, cwd=cwd).decode('utf8').strip()


def git_get_hash(p):
    return cmd(['git', 'rev-parse', 'HEAD'], p)


def git_log(p, sha):
    return cmd(['git', 'log', '--pretty=format:%s', sha + '..HEAD'], p)


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


def to_lib_dict(info):
    ret = {}
    for libs in info.values():
        for lib in libs:
            ret[lib.pkg] = lib.version
    return ret


def json_file():
    home = os.path.expanduser('~')
    return os.path.join(home, '.aur_deps.json')


def write_json_deps(args_name):
    # todo: allow partial writes...
    aur = aur_path()
    projects = find_git_folders(aur)
    store = {}
    if os.path.isfile(json_file()):
        with open(json_file(), 'r') as f:
            store = json.loads(f.read())
    for p in projects:
        name = get_project_name(p)
        if args_name == name or args_name == '-':
            print(name)
            map = {}
            map['git'] = git_get_hash(p)
            map['deps'] = to_lib_dict(pkg_info(p))
            store[name] = map
    print('Writing json to {}'.format(json_file()))
    with open(json_file(), 'w') as f:
        f.write(json.dumps(store, sort_keys=True, indent=4))
    print('done.')
    print()


#############################################################################

def handle_ls(args):
    aur = aur_path()
    projects = find_git_folders(aur)
    for p in projects:
        name = get_project_name(p)
        print(name)
        if args.all:
            print('Git:', git_info(p))
            info = pkg_info(p)
            for section, libs in info.items():
                print(section)
                for lib in libs:
                    print('  ', lib.pkg, lib.version)
            print()
    if not args.all:
        print()


def handle_check(args):
    aur = aur_path()
    projects = find_git_folders(aur)
    store = None
    if os.path.isfile(json_file()):
        with open(json_file(), 'r') as f:
            store = json.loads(f.read())
    else:
        print('Note:')
        print('Missing json file, less checks will be done')
        print()
    for p in projects:
        git_fetch(p)
        print(p, git_info(p))
        map = None
        if store is not None:
            name = get_project_name(p)
            if name in store:
                map = store[name]
            else:
                print('Missing stored information about', name)
        if map is not None:
            git = map['git']
            changes = git_log(p, git)
            if changes != '':
                print(changes)
                print()
            deps = map['deps']
            info = pkg_info(p)
            differs = False
            for section, libs in info.items():
                for lib in libs:
                    if not lib.pkg in deps or deps[lib.pkg] != lib.version:
                        print('  ', lib.pkg, section, 'differs')
                        differs = True
            if differs:
                print()


def handle_write(args):
    write_json_deps(args.name)


def handle_add(args):
    git = 'https://aur.archlinux.org/{}.git'.format(args.name)
    print('Adding ', git)
    subprocess.run(['git', 'clone', git], cwd=aur_path(), check=True)

def handle_git(args):
    aur = aur_path()
    projects = find_git_folders(aur)

    for p in projects:
        print('---------------------------')
        print('      ', get_project_name(p))
        run_git_update(p)
        print()


def get_backup_path():
    return os.path.join(os.path.dirname(get_src_folder()), 'backup-aur.json')


def handle_backup(args):
    backup_path = get_backup_path()
    aur = aur_path()
    projects = find_git_folders(aur)
    names = [get_project_name(p) for p in projects]
    store = {'projects': names}
    print('Backing up to ', backup_path)
    with open(backup_path, 'w') as f:
        f.write(json.dumps(store, sort_keys=True, indent=4))


def handle_install(args):
    aur = aur_path()
    projects = find_git_folders(aur)
    found = False

    for p in projects:
        if get_project_name(p) == args.app:
            found = True
            if args.clear:
                clear_pkg(p)
            install_pkg(p)
            write_json_deps(get_project_name(p))

    if not found:
        print('Invalid app ', aur)


def main():
    parser = argparse.ArgumentParser(description='aur helper tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('ls', help='list aur libraries')
    sub.add_argument('--all', '-a', action='store_true', help='include more information')
    sub.set_defaults(func=handle_ls)

    sub = sub_parsers.add_parser('check', help='check aur libraries for updates')
    sub.set_defaults(func=handle_check)

    sub = sub_parsers.add_parser('backup', help='do backup of aur to dotfiles')
    sub.set_defaults(func=handle_backup)

    sub = sub_parsers.add_parser('git', help='update the git repos')
    sub.set_defaults(func=handle_git)

    sub = sub_parsers.add_parser('add', help='add a new project')
    sub.add_argument('name', help='the aur project to add')
    sub.set_defaults(func=handle_add)

    sub = sub_parsers.add_parser('write', help='write current dependency status to json')
    sub.add_argument('name', help='the aur project to write, single - to mean all projects')
    sub.set_defaults(func=handle_write)

    sub = sub_parsers.add_parser('install', aliases=['in', 'up', 'update'], help='install or update the named aur dependency')
    sub.add_argument('app')
    sub.add_argument('--noclear', action='store_false', dest='clear')
    sub.set_defaults(func=handle_install)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

