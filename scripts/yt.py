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


def exec(cmd):
    subprocess.run(cmd)


def handle_single(args):
    for v in args.video:
        # youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' -i -o '%(title)s.%(ext)s' --restrict-filenames https://www.youtube.com/watch?v=vWaY7TqRzlg
        params = ["youtube-dl", "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", "--ignore-errors", "--output", "'%(title)s.%(ext)s'", "--restrict-filenames"]

        if args.keep:
            params += ['-k']

        params += [v]
        exec(params)


def handle_channel(args):
    # todo(Gustav): handle channel
    # youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' -i -o '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' --restrict-filenames --write-sub --sub-lang en --convert-subs srt --playlist-reverse --download-archive dan-root.txt https://www.youtube.com/user/rootay/videos

    params = [
        "youtube-dl",
        "-f",
        'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        "-i",
        "-o", '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s',
        "--restrict-filenames"
    ]

    if args.srt:
        params += ["--write-sub", "--sub-lang", "en", "--convert-subs", "srt"]
    
    if args.reverse:
        params += ['--playlist-reverse']

    if args.archive is not None:
        params += ["--download-archive", args.archive]

    params += [args.channel]
    exec(params)


# todo(Gustav): handle playlist
# youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' -i -o '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' --restrict-filenames --download-archive q-archive.txt https://www.youtube.com/playlist?list=PLFE56C0B2DE75289A


def main():
    parser = argparse.ArgumentParser(description='youtube offline')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('single', help='single video')
    sub.add_argument('video', nargs='+', help='the url of the videos')
    sub.add_argument('-k', '--keep', action='store_true', dest='keep', help='keep the intermediate')
    sub.set_defaults(func=handle_single)


    sub = sub_parsers.add_parser('channel', help='all videos from a channel')
    sub.add_argument('channel', help='the url of the video')
    sub.add_argument('--archive', help='archive file')
    sub.add_argument('--srt', action='store_true', help='add subtitles')
    sub.add_argument('--reverse', action='store_true', help='process it in reverse')
    sub.set_defaults(func=handle_channel)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()    
    except KeyboardInterrupt:
        exit()
