#!/usr/bin/env python3
#
# Copyright (C) 2017 Marcel Patzwahl
# Licensed under the terms of the GNU GPL v3 only.
#
# i3blocks blocklet script to see the available updates of pacman and the AUR
# modified by Gustav

import subprocess
import argparse


def get_updates():
    output = subprocess.check_output(['checkupdates']).decode('utf-8')
    if not output:
        return []

    updates = [line.split(' ')[0]
               for line in output.split('\n')
               if line]

    return updates


def get_aur_updates():
    output = ''
    try:
        output = subprocess.check_output(['yaourt', '-Qua']).decode('utf-8')
    except subprocess.CalledProcessError as exc:
        # yaourt exits with 1 and no output if no updates are available.
        # we ignore this case and go on
        if not (exc.returncode == 1 and not exc.output):
            raise exc
    if not output:
        return []

    aur_updates = [line.split(' ')[0]
                   for line in output.split('\n')
                   if line.startswith('aur/')]

    return aur_updates


def collect_all_updates(also_aur):
    updates = get_updates()
    if also_aur:
        updates += get_aur_updates()
    return updates


def message(bg, fg, text):
    print( "<span background='{0}' color='{1}'>{2}</span>".format(bg, fg, text))


def main():
    parser = argparse.ArgumentParser(description='Check for pacman updates')
    parser.add_argument(
        '-B',
        '--base_bg',
        default='white',
        help='base background of the output'
    )
    parser.add_argument(
        '-U',
        '--updates_available_bg',
        default='red',
        help='color of the background, when updates are available(default=white)'
    )
    parser.add_argument(
        '-b',
        '--base_color',
        default='black',
        help='base color of the text'
    )
    parser.add_argument(
        '-u',
        '--updates_available_color',
        default='white',
        help='color of the text, when updates are available'
    )
    parser.add_argument(
        '-a',
        '--aur',
        action='store_true',
        help='Include AUR packages. Attn: Yaourt must be installed'
    )
    parser.add_argument(
        '-q',
        '--quiet',
        action = 'store_true',
        help = 'Do not produce output when system is up to date'
    )
    parser.add_argument(
        '-c',
        '--critical_updates',
        default=0,
        type=int,
        help='Number of updates available before color is switched'
    )
    args = parser.parse_args()

    number_of_updates = len(collect_all_updates(args.aur))

    critical_updates = number_of_updates > args.critical_updates
    bg = args.updates_available_bg    if critical_updates else args.base_bg
    fg = args.updates_available_color if critical_updates else args.base_color

    if number_of_updates > 0:
        message(bg, fg, '{} updates available'.format(number_of_updates))
    elif not args.quiet:
        message(bg, fg, 'system up to date')


if __name__ == "__main__":
    main()

