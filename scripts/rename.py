#!/usr/bin/env python3

import argparse
import os


def handle_ext(args):
    ext = args.extension
    if ext[0] != '.':
        ext = '.' + ext
    for relative in args.files:
        from_path = os.path.abspath(os.path.realpath(relative))
        pre, _ = os.path.splitext(from_path)
        new_path = pre + ext
        os.rename(from_path, new_path)


def handle_lower(args):
    for relative in args.files:
        from_path = os.path.abspath(os.path.realpath(relative))
        pre, ext = os.path.splitext(from_path)
        head, tail = os.path.split(pre)
        tail = tail.lower()
        new_path = os.path.join(head, tail + ext)
        os.rename(from_path, new_path)


def handle_add_prefix(args):
    for relative in args.files:
        from_path = os.path.abspath(os.path.realpath(relative))
        pre, ext = os.path.splitext(from_path)
        head, tail = os.path.split(pre)
        if args.remove:
            if tail.startswith(args.prefix):
                tail = tail[len(args.prefix):]
        else:
            tail = args.prefix + tail
        new_path = os.path.join(head, tail + ext)
        if args.run:
            os.rename(from_path, new_path)
        else:
            print(new_path)


def main():
    parser = argparse.ArgumentParser(description='rename files')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('ext', help='change extension')
    sub.add_argument('extension', help="the new extension")
    sub.add_argument('files', nargs='+', help="the files to change")
    sub.set_defaults(func=handle_ext)

    sub = sub_parsers.add_parser('lower', help='change filename to small caps')
    sub.add_argument('files', nargs='+', help="the files to change")
    sub.set_defaults(func=handle_lower)

    sub = sub_parsers.add_parser('add-prefix', help='add prefix to files')
    sub.add_argument('prefix', help="the prefix to add")
    sub.add_argument('--remove', action="store_true", help="remove instead of add")
    sub.add_argument('--run', action="store_true", help="do the command instead of printing the new name")
    sub.add_argument('files', nargs='+', help="the files to change")
    sub.set_defaults(func=handle_add_prefix)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

