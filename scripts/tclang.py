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

class Header:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.parents = []
        self.children = []

def read_dot_file(path):
    with open(path) as f:
        r = {}
        lines = f.readlines()
        lines = [x.strip().rstrip(';') for x in lines if x.rstrip().endswith(';')]
        for l in lines:
            if '->' in l:
                links = l.split('->')
                parent = links[0].strip()
                child = links[1].strip()
                r[parent].children.append(child)
                r[child].parents.append(parent)

            else:
                name = l.split(' ', maxsplit=2)[0].strip()
                path = l.split('label=')[1].rstrip(']').strip('"').strip()
                r[name] = Header(name, path)
        return r


def get_key(data, search):
    if search in data:
        return search

    keys = []
    for h in data.values():
        if search in h.path:
            keys.append(h.name)

    if len(keys) == 1:
        return keys[0]
    elif len(keys) > 0:
        print('Search resulted in many entries...')
        for k in keys:
            d = data[k]
            print('*', d.name, d.path)

    return None


def print_tree(data, key, simple, reverse, step, lim):
    if lim >= 0 and lim < step:
        return
    d = data[key]
    n = d.name if not simple else ''
    p = d.path if not simple else os.path.basename(d.path)
    print('  '*step + n + " " + p)
    children = d.parents if reverse else d.children
    for c in children:
        print_tree(data, c, simple, reverse, step+1, lim)

def handle_tree(args):
    data = read_dot_file(args.dot)
    key = get_key(data, args.search)
    if key is None:
        print('Unable to use find key for', args.search)
        return
    print_tree(data, key, args.simple, args.reverse, 0, args.depth)


def main():
    parser = argparse.ArgumentParser(description='Clang tool')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('tree', help='tree command')
    sub.add_argument('dot', help="the dot output")
    sub.add_argument('search', help="the root of the tree")
    sub.add_argument('--reverse', action='store_true', help="reverse the output")
    sub.add_argument('--simple', action='store_true', help="only display the filename")
    sub.add_argument('--depth', default=-1, type=int, help="reverse the output")
    sub.set_defaults(func=handle_tree)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

