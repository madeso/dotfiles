#!/usr/bin/env python3
import os
import argparse


def read_lines(file):
    last_error = None
    for e in ['utf-8', 'cp1252']:
        try:
            with open(file, 'r', encoding=e) as f:
                return f.readlines()
        except UnicodeDecodeError as e:
            last_error = e
            print('ERROR: unicode error for', file)
    raise last_error


def fix_file(file, force, extensions):
    ext = os.path.splitext(file)[1][1:]
    if force or ext in extensions:
        print("fixing " + file)
        lines = read_lines(file)
        with open(file, 'wb') as f:
            for line in lines:
                f.write((line.rstrip() + "\n").encode('utf-8'))


def walk_dirs(path, extensions):
    for name in os.listdir(path):
        dir = os.path.join(path, name)
        fix_file_or_dir(dir, False, extensions)


def fix_file_or_dir(path, force, extensions):
    if os.path.isdir(path):
        walk_dirs(path, extensions)
    elif os.path.isfile(path):
        fix_file(path, force, extensions)
    else:
        print('neither dir nor file', path)


def main():
    parser = argparse.ArgumentParser(description="opens textfiles, converts to utf8 and LF with newline at the end")
    parser.add_argument('input', metavar='f', nargs='+', help='files or directories to clean')
    parser.add_argument('--extensions', default='c, cpp, cxx, h, hpp', help='extensions to use')
    args = parser.parse_args()
    extensions = [x.strip() for x in args.extensions.split(',')]
    for f in args.input:
        fix_file_or_dir(os.path.abspath(f), True, extensions)

if __name__ == "__main__":
    main()
