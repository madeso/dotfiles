#!/usr/bin/env python3

import argparse
import os
import subprocess
import shlex


###################################################################################################
# Functions


def get_files(dir: str) -> list[str]:
    files = []
    for root, dirs, fs in os.walk(dir, topdown=True, followlinks=False):
        for f in fs:
            if f.endswith('.wav'):
                files.append(os.path.join(root, f))
    return files


def mp3_file_from_wav(file: str) -> str:
    return os.path.splitext(file)[0] + '.mp3'


def convert_to_mp3(file: str, nop: bool) -> None:
    output = mp3_file_from_wav(file)
    if os.path.exists(output):
        print(f'Skipping {file} since it already exists')
        return
    # https://gist.github.com/dominicthomas/52e610c9cd4083408371
    cmd = ['ffmpeg', '-i', file, '-ab', '320k', '-ac', '2', '-ar', '44100', '-joint_stereo', '0', output]
    if nop:
        print(shlex.join(cmd))
    else:
        subprocess.run(cmd)


###################################################################################################
# Commands


def run_find(args):
    files = get_files(os.getcwd())
    for f in files:
        print(f)
    print(f'Found {len(files)} files')


def run_convert_single(args):
    convert_to_mp3(args.file, args.nop)


def run_convert_all(args):
    files = get_files(os.getcwd())
    for f in files:
        convert_to_mp3(f, args.nop)


def run_delete_all(args):
    files = get_files(os.getcwd())
    for f in files:
        mp3 = mp3_file_from_wav(f)
        if os.path.exists(mp3):
            if args.nop:
                print(f'Would delete {f}')
            else:
                os.remove(f)
                print(f'Deleted {f}')

###################################################################################################
# Main


def main():
    argparser = argparse.ArgumentParser(description='Convert wav to mp3')
    argparser.set_defaults(func=lambda args: argparser.print_help())

    subs = argparser.add_subparsers(dest='command')

    sub = subs.add_parser('find', help='List all wav files')
    sub.set_defaults(func=run_find)

    sub = subs.add_parser('single', help='Run convert on all wav files')
    sub.add_argument('file', help='Wav file to convert')
    sub.add_argument('--nop', action='store_true', help='Print command instead of running it')
    sub.set_defaults(func=run_convert_single)

    sub = subs.add_parser('all', help='Run convert on all wav files')
    sub.add_argument('--nop', action='store_true', help='Print command instead of running it')
    sub.set_defaults(func=run_convert_all)

    sub = subs.add_parser('delete', help='Delete all wav files that have a corresponding mp3 file')
    sub.add_argument('--nop', action='store_true', help='Print command instead of running it')
    sub.set_defaults(func=run_delete_all)

    args = argparser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
