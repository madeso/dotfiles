#!/usr/bin/env python3

import dotlib


def get_data():
    data = dotlib.Data()
    data.add_file('_vimrc', '.vimrc')
    data.add_file('_zshrc', '.zshrc')
    data.add_file('_xresources', '.Xresources')
    data.add_file('fonts.conf', '.config/fontconfig/fonts.conf')
    data.add_file('minttyrc', '.minttyrc')
    data.add_file('i3blocks-config', '.config/i3blocks/config')
    data.add_dir(
        dotlib.Dir("i3blocks-scripts", ".config/i3blocks/scripts")
          .file("arch-update.py")
          .file("disk_usage.sh")
          .file("load_average.sh")
          .file("volume-pulseaudio.sh")
    )
    data.add_file('gnome2', '.gtkrc-2.0')
    data.add_file('gnome3.ini', '.config/gtk-3.0/settings.ini')
    data.add_file('xinitrc', '.xinitrc')
    data.add_dir(
        dotlib.Dir("custom_fonts", ".fonts")
          .file("materialdesignicons-webfont.ttf")
    )
    data.add_dir(
        dotlib.Dir("vs_code", ".config/Code/User",
                   win_where=dotlib.PathType.APPDATA_ROAMING, win_home='Code\\User')
        .file('keybindings.json')
        .file('settings.json')
    )
    data.add_dir(
        dotlib.Dir('rofi', '.config/rofi')
        .file('config')
        .file('solarized-light.rasi')
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
