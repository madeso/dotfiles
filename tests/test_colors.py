#!/usr/bin/env python
import sys


def write_color_test(bold_flag, foreground_color, background_color, text):
    ESC = '\33'
    color_code = "[{};{};{}m".format(bold_flag, foreground_color, background_color)
    sys.stdout.write(ESC + color_code + text + ESC + "[m ")


def string_with_width(str, width):
    return '{0:{width}}'.format(str, width=width)


def string_ra(str, width):
    return '{0:>{width}}'.format(str, width=width)


def sample_text_width(text, sample_text, color_name):
    return string_with_width(text, max([len(color_name), len(sample_text)]))


# reference: https://en.wikipedia.org/wiki/ANSI_escape_code
def write_color_table(bold_flag, bright):
    sys.stdout.write("\n")
    sys.stdout.write('Normal' if bold_flag == 0 else 'Bold')
    if bright:
        sys.stdout.write(" [bright]")
    sys.stdout.write("\n")
    NAMES = ['Black', 'Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan', 'White', 'Default']
    color_name_width = max([len(name) for name in NAMES])
    sample_text = 'test'
    sys.stdout.write(string_ra('FG\\BG ', color_name_width + 1))
    max_color_count = 9 if not bright else 8
    for n in NAMES[0:max_color_count]:
        sys.stdout.write(sample_text_width(n, sample_text, n) + " ")
    sys.stdout.write("\n")
    for foreground_index in range(max_color_count):
        sys.stdout.write(string_ra(NAMES[foreground_index] + ' ', color_name_width + 1))
        for background_index in range(max_color_count):
            foreground_color = foreground_index + (30 if not bright else 90) + (1 if foreground_index == 8 else 0)
            background_color = background_index + (40 if not bright else 100) + (1 if background_index == 8 else 0)
            t = sample_text_width(sample_text, sample_text, NAMES[background_index])
            write_color_test(bold_flag, foreground_color, background_color, t)
        sys.stdout.write("\n")


def main():
    for bold_flag in [0, 1]:
        for bright in [False, True]:
            write_color_table(bold_flag, bright)

if __name__ == "__main__":
    main()
