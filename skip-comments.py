#!/usr/bin/env python3

import argparse


def skip_comments(words):
    found_comment = False
    for w in words:
        if found_comment == False:
            if w[0] == '#':
                found_comment = True
            else:
                yield w


def main():
    parser = argparse.ArgumentParser(description='skip comments and print each word on a line')
    parser.add_argument('infile', type=argparse.FileType('r'), help='the file to parse')
    args = parser.parse_args()

    f = args.infile
    for line in f:
        for word in skip_comments(line.strip().split()):
            print(word)


if __name__ == "__main__":
    main()

