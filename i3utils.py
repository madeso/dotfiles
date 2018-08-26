#!/usr/bin/env python3
import os
import argparse
import subprocess
import sys

def do_solarized_scope_replace(line):
  return line.format(
                     base03    ='#002b36',
                     base02    ='#073642',
                     base01    ='#586e75',
                     base00    ='#657b83',
                     base0     ='#839496',
                     base1     ='#93a1a1',
                     base2     ='#eee8d5',
                     base3     ='#fdf6e3',
                     yellow    ='#b58900',
                     orange    ='#cb4b16',
                     red       ='#dc322f',
                     magenta   ='#d33682',
                     violet    ='#6c71c4',
                     blue      ='#268bd2',
                     cyan      ='#2aa198',
                     green     ='#859900')

def do_line_scope_replace(line, scope):
  if scope == 'solarized':
    return do_solarized_scope_replace(line)
  return line

def get_config_lines():
  src = os.path.expanduser('~/dev/dotfiles/i3/config')
  lines = []
  
  scope = ''
  with open(src, 'r') as in_file:
    for l in in_file:
      line = l.rstrip()
      if line.lower().startswith('# starts section'):
        scope = line[16:].strip()
      if line.lower().startswith('# ends section'):
        scope = ''
      line = do_line_scope_replace(line, scope)
      lines.append(line)
  return lines

def write_config_lines():
  pass


def handle_print(args):
  lines = get_config_lines()
  for line in lines:
    print(line)

def i3_msg(cmd):
  subprocess.call(['i3-msg', cmd])

def handle_write(args):
  write_config_lines()

def handle_reload(args):
  write_config_lines()
  i3_msg('reload')

def handle_restart(args):
  write_config_lines()
  i3_msg('restart')

def main():
  parser = argparse.ArgumentParser(description='i3 utils')
  sub_parsers = parser.add_subparsers(dest='command_name')

  sub = sub_parsers.add_parser('print')
  sub.set_defaults(func=handle_print)

  sub = sub_parsers.add_parser('write')
  sub.set_defaults(func=handle_write)

  sub = sub_parsers.add_parser('reload')
  sub.set_defaults(func=handle_reload)

  sub = sub_parsers.add_parser('restart')
  sub.set_defaults(func=handle_restart)

  args = parser.parse_args()
  if args.command_name is not None:
    args.func(args)
  else:
    parser.print_help()
if __name__ == "__main__":
   main()
