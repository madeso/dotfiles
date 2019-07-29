#!/usr/bin/env python3

import argparse
import os
import typing
import json


def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def get_home_folder() -> str:
    return os.path.expanduser('~')


def get_config_file_name() -> str:
    return os.path.join(get_home_folder(), '.nas.json')


class Nas:
    def __init__(self):
        self.remote = ''
        self.local = ''
        self.cred = ''
        self.workgroup = ''

    def __str__(self):
        return  '{remote} {local} {cred} {workgroup}'.format(
            remote = self.remote,
            local = self.local,
            cred = self.cred,
            workgroup = self.workgroup
            )

    def tojson(self):
        js = {}
        js['remote'] = self.remote
        js['local'] = self.local
        js['cred'] = self.cred
        js['workgroup'] = self.workgroup
        return js


def fromjson(js):
    self = Nas()
    self.remote = js['remote']
    self.local = js['local']
    self.cred = js['cred']
    self.workgroup = js['workgroup']
    return self


def get_user_data() -> typing.List[Nas]:
    if file_exist(get_config_file_name()):
        with open(get_config_file_name(), 'r') as f:
            js =  json.loads(f.read())
            return [fromjson(di) for di in js]
    else:
        return []


def set_user_data(data: typing.List[Nas]):
    with open(get_config_file_name(), 'w') as f:
        print(json.dumps([d.tojson() for d in data], sort_keys=True, indent=4), file=f)


def remove_remote(data: typing.List[Nas], name: str) -> typing.List[Nas]:
    return [n for n in data if n.remote != name]


def handle_list(args):
    d = get_user_data()
    for n in d:
        print(n)
    print("{} item(s)".format(len(d)))


def handle_add(args):
    d = get_user_data()
    n = Nas()
    n.remote = args.remote
    n.local = args.local
    n.cred = args.cred
    n.workgroup = args.workgroup
    d = remove_remote(d, n.remote)
    d.append(n)
    set_user_data(d)


def handle_remove_remote(args):
    d = get_user_data()
    d = remove_remote(d, args.remote)
    set_user_data(d)


def handle_connect(args):
    d = get_user_data()
    for n in d:
        subprocess.check_output(['mount', '-t', 'cifs', n.remote, n.local, '-o', 'credentials={cred},workgroup={wg},iocharset=utf8,uid=gustav,vers=1.0'.format(cred=n.cred, wg=n.workgroup)])


def main():
    parser = argparse.ArgumentParser(description='connect nas and stuff')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('ls', help='Copy files to HOME')
    sub.set_defaults(func=handle_list)

    sub = sub_parsers.add_parser('connect', help='Copy files to HOME')
    sub.set_defaults(func=handle_connect)

    sub = sub_parsers.add_parser('remove', help='Copy files to HOME')
    sub.add_argument('remote', help='File pattern to diff')
    sub.set_defaults(func=handle_remove_remote)

    add = sub_parsers.add_parser('add', help='add nas')
    add.add_argument('remote', help='Remote path')
    add.add_argument('local', help='Local path')
    add.add_argument('cred', help='Credential file')
    add.add_argument('workgroup', help='workgroup')
    add.set_defaults(func=handle_add)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

