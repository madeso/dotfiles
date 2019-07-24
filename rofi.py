#!/usr/bin/env python3

import subprocess
import typing

def show(input) -> typing.Optional[str]:
   v = subprocess.run(['rofi', '-dmenu'], stdout=subprocess.PIPE, input='\n'.join(input), encoding='utf8')
   if v.returncode == 0:
       return v.stdout.strip()
   else:
       return None


def test_show():
   print(show(['tabbed', 'stacking']))


def select(input):
    strings = []
    for name in input:
        strings.append(name)
    sel = show(strings)
    if sel is not None:
        input[sel]()


def test_select():
    select({'tabbed': lambda: print('tabby cat'), 'stacked': lambda: print('stacking boxes')})


def cmd(input):
    l = {}
    for name in input:
        def create_cmd(cmd):
            return lambda: subprocess.run(cmd)
        l[name] = create_cmd(input[name])
    select(l)


def test_cmd():
    cmd({'list': ['ls'], 'all': ['ls', '-a'], 'clear': ['clear']})


def main():
    import argparse
    parser = argparse.ArgumentParser(description='rofi.py cli test')
    sub = parser.add_subparsers()
    parser.set_defaults(func=None)
    sub.add_parser('show').set_defaults(func=test_show)
    sub.add_parser('select').set_defaults(func=test_select)
    sub.add_parser('cmd').set_defaults(func=test_cmd)
    args = parser.parse_args()
    if args.func is None:
        parser.print_help()
    else:
        args.func()

if __name__ == "__main__":
    main()
