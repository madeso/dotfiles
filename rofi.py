#!/usr/bin/env python3

import subprocess
import typing

def rofi(input) -> typing.Optional[str]:
   v = subprocess.run(['rofi', '-dmenu'], stdout=subprocess.PIPE, input='\n'.join(input), encoding='utf8')
   if v.returncode == 0:
       return v.stdout.strip()
   else:
       return None

if __name__ == "__main__":
   print(rofi(['tabbed', 'stacking']))
