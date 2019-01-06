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

if __name__ == "__main__":
    test_select()
