#!/usr/bin/env python3

import argparse
import os
import typing
import json
import datetime
import re


def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def get_home_folder() -> str:
    return os.path.expanduser('~')


def get_config_file_name() -> str:
    return os.path.join(get_home_folder(), '.sometimes.json')


def get_user_data() -> typing.Dict[str, str]:
    if file_exist(get_config_file_name()):
        with open(get_config_file_name(), 'r') as f:
            return json.loads(f.read())
    else:
        return {}


def set_user_data(data: typing.Dict[str, str]):
    with open(get_config_file_name(), 'w') as f:
        print(json.dumps(data, sort_keys=True, indent=4), file=f)


# from: https://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string
regex = re.compile(
        r'((?P<days>\d+?)d)?'+
        r'((?P<hours>\d+?)hr)?'+
        r'((?P<minutes>\d+?)m)?'+
        r'((?P<seconds>\d+?)s)?'
        )
def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        print('time string is not valid')
        return None
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return datetime.timedelta(**time_params)


def main():
    parser = argparse.ArgumentParser(description='Manage my dot files.')
    parser.add_argument('app')
    parser.add_argument('timespan')
    parser.add_argument('--debug', '-d', action='store_true')
    args = parser.parse_args()
    data = get_user_data()
    delta = parse_time(args.timespan)
    if args.debug:
        print('timespan:', delta)
    if delta is None:
        return
    if delta <= datetime.timedelta(seconds=1):
        print('timespan is too short')
        return
    if args.app in data:
        then = datetime.datetime.fromisoformat(data[args.app])
        future = then + delta 
        now = datetime.datetime.now()
        if args.debug:
            print('Recorded:', then)
            print('Have to pass:', future)
            print('Now:', now)

        if future < now:
            data[args.app] = datetime.datetime.now().isoformat()
            set_user_data(data)
            if args.debug:
                print('passed')
            exit(0)
        else:
            if args.debug:
                print('rejected')
            exit(-1)
    else:
        data[args.app] = datetime.datetime.now().isoformat()
        set_user_data(data)
        if args.debug:
            print('passed')
        exit(0)


if __name__ == "__main__":
    main()

