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

#=================================
# settings type

class Settings:
    def __init__(self, name, default_value):
        self.name = name
        self.default_value = default_value
    
    def get_value(self, data):
        if not self.name in data:
            return self.default_value
        else:
            return data[self.name]
    
    def set_value(self, data, value):
        data[self.name] = value

    def set_defualt_if_missing(self, data):
        if not self.name in data:
            data[self.name] = self.default_value


#==================================
# settings
SETTINGS_GOURCE_PATH = Settings('gource_path', 'gource')

# config
CONFIG_SECONDS_PER_DAY = Settings('seconds_per_day', 10)
CONFIG_AUTOSKIP_SECONDS = Settings('autoskip_seconds', 3)
CONFIG_FILE_IDLE_TIME = Settings('file_idle_time', 60)
CONFIG_MAX_FILE_LAG = Settings('max_file_lag', 5)
CONFIG_DATE_FORMAT = Settings('date_format', '')
CONFIG_HIDE = Settings('hide', [])

#==================================
# common functions
def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def get_home_folder() -> str:
    return os.path.expanduser('~')


def get_config_file_name() -> str:
    return os.path.join(get_home_folder(), '.tgource.json')


def get_user_data() -> typing.Dict[str, str]:
    if file_exist(get_config_file_name()):
        with open(get_config_file_name(), 'r') as f:
            return json.loads(f.read())
    else:
        return {}


def set_user_data(data: typing.Dict[str, str]):
    with open(get_config_file_name(), 'w') as f:
        print(json.dumps(data, sort_keys=True, indent=4), file=f)


#======================================
# tool gource functions

def value_or_default(data, name, default):
    if not name in data:
        return default
    else:
        return data[name]


def get_gource_path():
    return SETTINGS_GOURCE_PATH.get_value(get_user_data())


def has_gource(p=None):
    try:
        subprocess.check_output([get_gource_path() if p is None else p, '--help'])
        # todo(Gustav): check version of gource too...
        return True
    except FileNotFoundError:
        return False


def get_project_file_name(folder) -> str:
    return os.path.join(folder, '.tgource.json')


def get_project_data(folder) -> typing.Dict[str, str]:
    if file_exist(get_project_file_name(folder)):
        with open(get_project_file_name(folder), 'r') as f:
            return json.loads(f.read())
    else:
        return {}


def set_project_data(folder, data: typing.Dict[str, str]):
    with open(get_project_file_name(folder), 'w') as f:
        print(json.dumps(data, sort_keys=True, indent=4), file=f)


def is_git_folder(folder):
    config = os.path.join(folder, '.git', 'config')
    return file_exist(config)


#=================================
# commandline callbacks

def handle_setup(args):
    if not has_gource():
        print('Note: Missing gource')
        p = args.path
        if p is None:
            print('Error: No path specified!')
            return
        if has_gource(p):
            print('new path looks good')
            data = get_user_data()
            SETTINGS_GOURCE_PATH.set_value(data, p)
            set_user_data(data)
        else:
            print('Error: Inalid path to gource: {}'.format(p))
    else:
        print("You have gource installed, you're good to go")


def handle_init(args):
    if not has_gource():
        print('Error: Missing gource, run setup')
        return
    folder = args.folder
    if not is_git_folder(folder):
        print('Error: non git folder are not supported')
        return
    settings = get_project_data(folder)
    if args.force:
        settings = {}
    configs = [CONFIG_SECONDS_PER_DAY, CONFIG_AUTOSKIP_SECONDS, CONFIG_FILE_IDLE_TIME, CONFIG_MAX_FILE_LAG, CONFIG_HIDE, CONFIG_DATE_FORMAT]
    for c in configs:
        c.set_defualt_if_missing(settings)
    if args.hide:
        CONFIG_HIDE.set_value(settings, ['bloom','date','dirnames','files','filenames','mouse','progress','tree','users','usernames'])
    if args.sane_date:
        CONFIG_DATE_FORMAT.set_value(settings, '%Y-%m-%d')
    set_project_data(folder, settings)


def handle_run(args):
    if not has_gource():
        print('Error: Missing gource, run setup')
        return
    folder = args.folder
    if not is_git_folder(folder):
        print('Error: non git folder are not supported')
        return
    settings = get_project_data(folder)
    
    cmdline = [get_gource_path()]
    cmdline.extend(['--seconds-per-day', str(CONFIG_SECONDS_PER_DAY.get_value(settings))])
    if CONFIG_AUTOSKIP_SECONDS.get_value(settings) <= 0:
        cmdline.append('--disable-auto-skip')
    else:
        cmdline.extend(['--auto-skip-seconds', str(CONFIG_AUTOSKIP_SECONDS.get_value(settings))])
    cmdline.extend(['--file-idle-time', str(max(0, CONFIG_FILE_IDLE_TIME.get_value(settings)))])
    cmdline.extend(['--max-file-lag', str(CONFIG_MAX_FILE_LAG.get_value(settings))])
    if CONFIG_DATE_FORMAT.get_value(settings) != '':
        cmdline.extend(['--date-format', CONFIG_DATE_FORMAT.get_value(settings)])
    if len(CONFIG_HIDE.get_value(settings)) != 0:
        cmdline.extend(['--hide', ','.join(CONFIG_HIDE.get_value(settings))])
    
    print(cmdline)
    subprocess.run(cmdline, cwd=folder)


#==============================
# main

def main():
    parser = argparse.ArgumentParser(description='Gource helper tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('setup', help='setup settings')
    sub.add_argument('-p', '--path')
    sub.set_defaults(func=handle_setup)

    sub = sub_parsers.add_parser('init', help='init the project file')
    sub.add_argument('-f', '--force', action='store_true', help='if config exist, force overwrite')
    sub.add_argument('--hide', action='store_true', help='hide all elements')
    sub.add_argument('--sane-date', action='store_true', help='set dateformat to something same')
    sub.add_argument('--folder', help='the folder where to run from', default=os.getcwd())
    sub.set_defaults(func=handle_init)

    sub = sub_parsers.add_parser('run', help='run gource with the settings')
    sub.add_argument('--folder', help='the folder where to run from', default=os.getcwd())
    sub.set_defaults(func=handle_run)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

