#!/usr/bin/env python3

import dotlib


def get_data():
  return dotlib.Data(interesting_files = [dotlib.Path('_vimrc', '.vimrc')],
                     interesting_directories = [dotlib.Path('vimfiles', '.vim')])

if __name__ == "__main__":
    dotlib.main(get_data())
