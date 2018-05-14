#!/usr/bin/env python3

import dotlib


def get_data():
    data = dotlib.Data()
    data.add_file('_vimrc', '.vimrc')
    data.add_file('_minttyrc', '.minttyrc')
    data.add_dir(
        dotlib.Dir("vs_code", ".config/Code/User",
                   win_where=dotlib.PathType.APPDATA_ROAMING, win_home='Code\\User')
        .file('keybindings.json')
        .file('settings.json')
    )
    data.add_dir(
        dotlib.Dir('vimfiles', '.vim')
        .set_dir('colors')
        .file('solarized.vim')
        .set_dir('bitmaps')
        .file('togglebg.png')
        .set_dir('autoload')
        .file('togglebg.vim')
        .set_dir('after/ftplugin')
        .file('proto.vim')
    )
    return data


if __name__ == "__main__":
    dotlib.main(get_data())
