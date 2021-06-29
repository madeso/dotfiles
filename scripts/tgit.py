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

DATA_LIST = 'list'
DATA_COMMITS = 'commits'
COMMIT_DATE = 'date'
COMMIT_TEXT = 'text'
COMMIT_ERROR = 'error'
COMMIT_STATE = 'state'
# 0: unknown, 1: failed, 2: passed

STATE_UNKNOWN = 0
STATE_FAILED = 1
STATE_PASSED = 2


def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def get_config_file_name() -> str:
    return os.path.join(os.getcwd(), '.tgit.json')


def get_data():
    if file_exist(get_config_file_name()):
        with open(get_config_file_name(), 'r') as f:
            return json.loads(f.read())
    else:
        return {}


def set_data(data):
    with open(get_config_file_name(), 'w') as f:
        print(json.dumps(data, sort_keys=True, indent=4), file=f)


def error(message):
    print(message)
    sys.exit(-1)


def create_data_from_git():
    cmd = ['git', 'log', '--format=%H:%ct:%s']
    output = subprocess.check_output(cmd, encoding='utf-8').split('\n')
    data = [line.split(':', maxsplit=2) for line in output if len(line.strip()) > 0]
    ordered_commits = [line[0] for line in data]
    commits = {d[0]: {COMMIT_DATE: int(d[1]), COMMIT_TEXT: d[2], COMMIT_STATE: STATE_UNKNOWN, COMMIT_ERROR: ''} for d in data}
    r = {DATA_LIST: ordered_commits, DATA_COMMITS: commits}
    return r


def handle_setup(args):
    set_data(create_data_from_git())


def status_string(current, total):
    return f'{current} ({current/total*100:.2f}%)'


def get_commit_state(c):
    if COMMIT_STATE in c:
        return c[COMMIT_STATE]
    else:
        return 0


def require_data():
    data = get_data()
    if DATA_COMMITS not in data:
        error('please run setup')
    return data


def handle_status(args):
    data = require_data()

    commits = list(data[DATA_COMMITS].values())
    unknown_commits = [c for c in commits if get_commit_state(c) == STATE_UNKNOWN]
    failed_commits = [c for c in commits if get_commit_state(c) == STATE_FAILED]
    passed_commits = [c for c in commits if get_commit_state(c) == STATE_PASSED]
    total_commits = len(commits)
    print(f"{total_commits} number of commits")
    print(f"{status_string(len(unknown_commits), total_commits)} unknown")
    print(f"{status_string(len(failed_commits), total_commits)} failed")
    print(f"{status_string(len(passed_commits), total_commits)} passed")
    print()


def run_commit_lint(commit):
    runner = subprocess.run(['npx', 'commitlint'], input=commit[COMMIT_TEXT], encoding='utf-8', stdout=subprocess.PIPE)
    commit[COMMIT_ERROR] = runner.stdout.strip()
    commit[COMMIT_STATE] = STATE_PASSED if runner.returncode == 0 else STATE_FAILED


def get_string(msg: str) -> str:
    print(msg, end='> ')
    return input().strip()


def print_git_history(git_hash: str):
    output = subprocess.check_output(['git', 'show', git_hash], encoding='utf=8')
    print(output)


def handle_fix(args):
    data = require_data()
    ordered = data[DATA_LIST]
    commits = data[DATA_COMMITS]
    todo_commits = [k for k in ordered if get_commit_state(commits[k]) != STATE_PASSED]

    total = len(todo_commits)
    worked = 0
    try:
        for k in todo_commits:
            has_displayed_git = False
            c = commits[k]

            print('*' * 80)

            for _ in range(5):
                print()

            if get_commit_state(c) == STATE_UNKNOWN:
                run_commit_lint(c)

            while get_commit_state(c) != STATE_PASSED:
                for _ in range(3):
                    print()
                if has_displayed_git == False:
                    print_git_history(k)
                    has_displayed_git = True
                    print()
                print(c[COMMIT_TEXT])
                if COMMIT_ERROR in c:
                    print()
                    print(c[COMMIT_ERROR])
                command = get_string('').strip()
                
                if len(command) > 0 and command[0] == '+':
                    command = command.lstrip('+').strip() + ' ' + c[COMMIT_TEXT]
                
                if len(command)>0:
                    c[COMMIT_TEXT] = command
                    run_commit_lint(c)
            
            data[k] = c
            worked += 1
            print(f'{status_string(worked, total)}/{total}')
    finally:
        data[DATA_COMMITS] = commits
        set_data(data)

    command = get_string('')
    print(command)


def handle_check(args):
    data = require_data()
    ordered = data[DATA_LIST]
    commits = data[DATA_COMMITS]
    unknown_commits = [k for k in ordered if get_commit_state(commits[k]) == STATE_UNKNOWN]
    total = len(unknown_commits)
    worked = 0
    try:
        for k in unknown_commits:
            c = commits[k]
            run_commit_lint(c)
            worked += 1
            data[k] = c
            print(f'{status_string(worked, total)}/{total}')
    finally:
        data[DATA_COMMITS] = commits
        set_data(data)


def main():
    parser = argparse.ArgumentParser(description='Opinionated git tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('setup', help='setup the git logs')
    sub.set_defaults(func=handle_setup)

    sub = sub_parsers.add_parser('stat', help='get current status of the logs')
    sub.set_defaults(func=handle_status)

    sub = sub_parsers.add_parser('fix', help='fix logs')
    sub.set_defaults(func=handle_fix)

    sub = sub_parsers.add_parser('check', help='check all commits')
    sub.set_defaults(func=handle_check)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()

