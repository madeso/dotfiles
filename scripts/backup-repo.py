#!/usr/bin/env python3

import argparse
import os
import subprocess

def print_git_info(folder, script, i, actions):
    text = subprocess.run(['git', 'status', '--porcelain=1'], cwd=folder, capture_output=True, text=True).stdout.splitlines()
    has_changes = len(text) > 0
    if has_changes:
        print(f'{i}{folder} has {len(text)} git changes.')
        actions.append(f'GIT: You need to commit changes in {folder}')

    text = subprocess.run(['git', 'status'], cwd=folder, capture_output=True, text=True).stdout.splitlines()
    need_push = any(l.startswith('Your branch is ahead of') for l in text)

    if need_push:
        actions.append(f'GIT: {folder} needs a push')
        print(f'{i}{folder} needs a push')

    
    text = subprocess.run(['git', 'remote', '-v'], cwd=folder, capture_output=True, text=True).stdout.splitlines()
    repos = list(set(line.split()[1] for line in text))
    print(f'{i}{folder} has {len(repos)} git repos: {", ".join(repos)}.')
    repo_name = os.path.relpath(folder, os.getcwd())
    if len(repos)==1:
        script.append(f'git clone {repos[0]} {repo_name}')
    else:
        actions.append(f'GIT: {folder} doesnt have a single remote, actio needed')



def dobackup(dir, depth, indent, script, actions):
    i = ' ' * (indent * 4)
    entries = list(os.listdir(dir))
    if '.git' in entries:
        print(f'{i}{dir} is a git repo.')
        print_git_info(dir, script, i+'    ', actions)
        return
    print(f"{i}{dir} has {len(entries)} entries.")
    if depth == 0:
        actions.append(f'{dir} needs backup')
        return
    for f in entries:
        path = os.path.join(dir, f)
        if os.path.isdir(path):
            dobackup(path, depth-1, indent+1, script, actions)
        else:
            print(f'{i}    {f} is a file.')
            actions.append(f'{f} needs to be backed up')


def backup(args):
    script = []
    actions = []

    dobackup(os.getcwd(), 1, 0, script, actions)
    actions.sort()
    script.sort()

    if args.target_script:
        with open(args.target_script, 'w') as f:
            f.write('\n'.join(script))

    print()
    print("ACTIONS:")
    print('\n'.join(actions))


def main():
    argparser = argparse.ArgumentParser(description='Backup repo.')
    argparser.set_defaults(func=lambda args: argparser.print_help())

    subs = argparser.add_subparsers(dest='command')

    sub = subs.add_parser('backup', help='Backup repo.')
    sub.add_argument('--target-script', help='Script to write clone commands')
    sub.set_defaults(func=backup)

    args = argparser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
