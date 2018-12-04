#!/usr/bin/env python
import sys

# reference: https://en.wikipedia.org/wiki/ANSI_escape_code
def main():
    write = sys.stdout.write
    NAMES = ['Black', 'Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan', 'White']
    for bold_flag in range(2):
        for foreground_color in range(30, 38):
            for background_color in range(40, 48):
                write("\33[%d;%d;%dm%d;%d;%d\33[m " % (bold_flag, foreground_color, background_color, bold_flag, foreground_color, background_color))
            write("\n")


if __name__ == "__main__":
    main()
