#!/usr/bin/env python3

import dotlib


def get_data():
    data = dotlib.Data()

    # usage aliases
    data.set_var_alias(
        comments='base1', secondary='base1',
        background='base3',
        body='base00', text='base00', default='base00', code='base00', primary='base00', content='base00',
        emph='base01',
        highlights='base2'
    )

    # console color aliases
    data.set_var_alias(
        black='base02',
        white='base2',
        brblack='base03',
        brred='orange',
        brgreen='base01',
        bryellow='base00',
        brblue='base0',
        brmagenta='violet',
        brcyan='base1',
        brwhite='base3'
    )

    # color names
    data.set_vars(
        base02='#073642',
        red='#dc322f',
        green='#859900',
        yellow='#b58900',
        blue='#268bd2',
        magenta='#d33682',
        cyan='#2aa198',
        base2='#eee8d5',
        base03='#002b36',
        orange='#cb4b16',
        base01='#586e75',
        base00='#657b83',
        base0='#839496',
        violet='#6c71c4',
        base1='#93a1a1',
        base3='#fdf6e3'
    )

    data.add_file('vimrc', '.vimrc')
    data.add_file('zshrc', '.zshrc')
    data.add_file('xresources', '.Xresources')
    data.add_file('fonts.conf', '.config/fontconfig/fonts.conf')
    data.add_generated_file('i3config', '.config/i3/config')
    data.add_generated_file('minttyrc', '.minttyrc')
    data.add_generated_file('i3blocks-config', '.config/i3blocks/config')
    data.add_dir(
        dotlib.Dir("i3blocks-scripts", ".config/i3blocks/scripts")
          .file("arch-update.py")
          .file("disk_usage.sh")
          .file("load_average.sh")
          .file("volume-pulseaudio.sh")
          .file("keyboard-map.sh")
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
        .file('pathogen.vim')
        .set_dir('after/ftplugin')
        .file('proto.vim')
        .add_dir('bundle/syntastic/')
    )
    return data


if __name__ == "__main__":
    dotlib.main(get_data())
