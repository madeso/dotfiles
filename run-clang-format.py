#!/usr/bin/python3
import argparse
import subprocess
import os

parser = argparse.ArgumentParser(description='Run clang format and other stuff')
parser.add_argument('files', nargs='+', help='filenames')
args = parser.parse_args()

for f in args.files:
  ext = os.path.splitext(f)[1]
  if ext == '.cc' or ext == '.h':
    path =  os.path.abspath(f)
    subprocess.check_output(['clang-format', '-i', path])

