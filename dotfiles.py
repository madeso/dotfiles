#!/usr/bin/env python3

import os
import dotlib

def get_data():
    """get my settings"""
    data = dotlib.Data()

    # usage aliases
    #     comments='base1', secondary='base1',
    #     background='base3',
    #     body='base00', text='base00', default='base00', code='base00', primary='base00', content='base00',
    #     emph='base01',
    #     highlights='base2'

    # console color aliases
    #     black='base02',
    #     white='base2',
    #     brblack='base03',
    #     brred='orange',
    #     brgreen='base01',
    #     bryellow='base00',
    #     brblue='base0',
    #     brmagenta='violet',
    #     brcyan='base1',
    #     brwhite='base3'

    # color names
    #     base02='#073642',
    #     red='#dc322f',
    #     green='#859900',
    #     yellow='#b58900',
    #     blue='#268bd2',
    #     magenta='#d33682',
    #     cyan='#2aa198',
    #     base2='#eee8d5',
    #     base03='#002b36',
    #     orange='#cb4b16',
    #     base01='#586e75',
    #     base00='#657b83',
    #     base0='#839496',
    #     violet='#6c71c4',
    #     base1='#93a1a1',
    #     base3='#fdf6e3'

    # material colors
    # source: https://material.io/design/color/#color-theme-creation
    #     # primary main/variant, secondary main/variant, error main
    #     mat_prim='#6200EE',
    #     mat_priv='#3700B3',
    #     mat_secm='#03DAC6',
    #     mat_secv='#018786',
    #     mat_errm='#B00020',
    #     # on primary, on secondary, on error
    #     mat_opri='#FFFFFF',
    #     mat_osec='#000000',
    #     mat_oerr='#FFFFFF',
    #     junk='#FFFF00'

    general = ['general']
    arch = ['arch']
    zsh = ['zsh']
    win = ['win']
    code = ['code']
    gnome = ['gnome']

    # on linux this should be ~/.local/share/nvim/
    data.add_dir(dotlib.Dir(general, 'nvim', '.config/nvim', win_where=dotlib.PathType.APPDATA_LOCAL, win_home='nvim')
                 .file('init.lua')
                 .set_dir('lua/madeso')
                 .file('colorscheme.lua')
                 .file('statusline.lua')
                 )

    data.add_file(general, 'vimrc', '.vimrc')
    data.add_file(zsh, 'zshrc', '.zshrc')
    data.add_dir(
        dotlib.Dir(arch, 'kitty', '.config/kitty')
        .file('kitty.conf')
        .file('kitty-solarized-light.conf')
    )
    data.add_file(arch, 'xresources', '.Xresources')
    data.add_file(arch, 'powermate.toml', '.config/powermate.toml')
    data.add_file(arch, 'ranger.conf', '.config/ranger/rc.conf')
    # data.add_file(arch, 'termite.conf', '.config/termite/config') # no longer used
    data.add_file(arch, 'fonts.conf', '.config/fontconfig/fonts.conf')
    # data.add_file(arch, 'i3config', '.config/i3/config')
    data.add_file(arch, 'i3config_clean', '.config/i3/config')
    data.add_file(win, 'minttyrc', '.minttyrc')
    data.add_file(arch, 'dunst.cfg', '.config/dunst.cfg')
    data.add_file(arch, 'i3blocks-config', '.config/i3blocks/config')
    data.add_dir(
        dotlib.Dir(arch, "i3blocks-scripts", ".config/i3blocks/scripts")
          .file("arch-update.py")
          .file("disk_usage.sh")
          .file("load_average.sh")
          .file("volume-pulseaudio.sh")
          .file("keyboard-map.sh")
          .file("sensors.py")
    )
    data.add_file(gnome, 'gnome2', '.gtkrc-2.0')
    data.add_file(gnome, 'gnome3.ini', '.config/gtk-3.0/settings.ini')
    data.add_file(arch, 'xprofile', '.xprofile')
    data.add_dir(
        dotlib.Dir(arch, "custom_fonts", ".fonts")
          .file("materialdesignicons-webfont.ttf")
    )
    data.add_dir(
        dotlib.Dir(code, "vs_code", ".config/{}/User"
            .format('Code - OSS' if dotlib.has_class('arch') else 'Code'),
                   win_where=dotlib.PathType.APPDATA_ROAMING, win_home='Code' + os.path.sep + 'User', osx_home='Library/Application Support/Code/User')
        .file('keybindings.json')
        .file('settings.json')
    )
    data.add_dir(
        dotlib.Dir(arch, 'rofi', '.config/rofi')
        .file('config')
        .file('solarized-light.rasi')
    )
    data.add_file(arch, 'rofi/google-material.rasi', '.config/rofi/google-material.rasi')
    data.add_dir(
        dotlib.Dir(arch, 'shortcuts', '.local/share/applications')
            .file('dia-integrated.desktop')
            .file('maim-snip.desktop')
            .file('maim-screenshot.desktop')
            .file('maim-window-shadow.desktop')
    )
    data.add_dir(
        dotlib.Dir(arch, 'services', '.config/systemd/user')
            .file('ssh-agent.service')
    )
    data.add_file(arch, 'pam_environment', '.pam_environment')
    data.add_dir(
        dotlib.Dir(general, 'vimfiles', '.vim')
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
    data.add_file(win, 'powershell.ps1', 'Documents/PowerShell/Microsoft.PowerShell_profile.ps1')

    if dotlib.is_windows():
        # determine terminal name
        containing_folder_type = dotlib.PathType.APPDATA_LOCAL
        containing_folder = os.path.join(dotlib.get_folder(containing_folder_type), 'Packages')
        all_dirs = get_all_dirs(containing_folder)
        dirs = [d for d in all_dirs if 'Microsoft.WindowsTerminal' in d]
        if len(dirs) == 1:
            terminal_name = dirs[0].split(os.path.sep)[-1]
            print(f'Found terminal name: {terminal_name}')
            # todo(Gustav): add ignore sections/keys
            data.add_file_path(win, 'windows-terminal.json', f'Packages/{terminal_name}/LocalState/settings.json',
                            containing_folder_type)
        else:
            print(f'Error: found {len(dirs)} terminal folders: {dirs}')

    return data


def get_all_dirs(d):
    return [os.path.join(d, o) for o in os.listdir(d) 
                    if os.path.isdir(os.path.join(d,o))]


if __name__ == "__main__":
    dotlib.main(get_data())
