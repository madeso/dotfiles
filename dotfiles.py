#!/usr/bin/env python3

import dotlib


def get_data():
    data = dotlib.Data(interesting_files = [dotlib.Path('_vimrc', '.vimrc')],
                       interesting_directories = [dotlib.Path('vimfiles', '.vim')])
    data.add_dir(
        dotlib.Dir("vs_code", ".config/Code/User")
        .file('keybindings.json')
        .file('settings.json')
    )
    return data

if __name__ == "__main__":
    dotlib.main(get_data())
