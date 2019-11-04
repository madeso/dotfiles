#!/usr/bin/env python3
import argparse
import json
import typing
import os
import datetime
import urllib.request


########################################################################################################################
# Common functions

def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def get_home_folder() -> str:
    return os.path.expanduser('~')


def get_config_file_name() -> str:
    return os.path.join(get_home_folder(), '.tpocket.json')


def get_user_data() -> typing.Dict[str, str]:
    if file_exist(get_config_file_name()):
        with open(get_config_file_name(), 'r', encoding="utf-8") as f:
            return json.loads(f.read())
    else:
        return {}


def set_user_data(data: typing.Dict[str, str]):
    with open(get_config_file_name(), 'w', encoding="utf-8") as f:
        print(json.dumps(data, sort_keys=True, indent=4), file=f)


class Settings:
    def __init__(self, name, default_value):
        self.name = name
        self.default_value = default_value

    def get_value(self, data):
        if self.name not in data:
            return self.default_value
        else:
            return data[self.name]

    def set_value(self, data, value):
        data[self.name] = value

    def set_defualt_if_missing(self, data):
        if self.name not in data:
            data[self.name] = self.default_value


def s(ss: str) -> str:
    if os.name == 'nt':
        return ss.encode().decode(encoding='1252', errors='ignore')
    else:
        return ss


########################################################################################################################
# Settings

REQUEST_TOKEN = Settings('request_token', '')
ACCESS_TOKEN = Settings('access_token', '')
USERNAME = Settings('username', '')


########################################################################################################################
# Pocket functions

# reference: https://getpocket.com/developer/docs/v3/retrieve

POCKET_CONSUMER_KEY = '88378-7e4d291dcf51de39675f5caa'
POCKET_REQUEST = 'https://getpocket.com/v3/oauth/request'
POCKET_AUTH = 'https://getpocket.com/v3/oauth/authorize'
POCKET_GET = 'https://getpocket.com/v3/get'


def get_pocket_request(url, data):
    r = urllib.request.Request(url=url, method='POST')
    r.add_header('Content-Type', 'application/json; charset=UTF8')
    r.add_header('X-Accept', 'application/json')
    data_encoded = json.dumps(data).encode('utf-8')
    with urllib.request.urlopen(r, data_encoded) as f:
        return json.loads(f.read().decode('utf-8'))


def get_cache_file_name() -> str:
    return os.path.join(get_home_folder(), '.tpocket.cache.json')


class Post:
    def __init__(self, postid, post):
        self.id = postid
        self.title = post['given_title']
        if len(self.title) < 1:
            self.title = post['resolved_title']
        self.added = datetime.date.fromtimestamp(int(post['time_added']))
        self.excerpt = post['excerpt']
        self.url = post['resolved_url']


def get_all_pockets_data():
    data = get_user_data()

    if ACCESS_TOKEN.get_value(data) == '':
        return []
    if file_exist(get_cache_file_name()):
        # todo(Gustav): check for latest if enought time has passed
        with open(get_cache_file_name(), 'r', encoding="utf-8") as f:
            return json.loads(f.read())
    else:
        request_data = {
            'consumer_key': POCKET_CONSUMER_KEY,
            'access_token': ACCESS_TOKEN.get_value(data)
        }
        gets = get_pocket_request(POCKET_GET, request_data)
        with open(get_cache_file_name(), 'w', encoding="utf-8") as f:
            print(json.dumps(gets, sort_keys=True, indent=4), file=f)
        return gets


def get_all_pockets(args) -> typing.List[Post]:
    data = get_all_pockets_data()
    ret = []
    for postid, post in data['list'].items():
        add = True
        post = Post(postid, post)

        if args.filter != '' and args.filter not in post.url:
            add = False

        if add:
            ret.append(post)

    return ret


########################################################################################################################
# handler functions

def handle_setup(args):
    data = get_user_data()

    if REQUEST_TOKEN.get_value(data) == '':
        print('Getting request token...')
        request_data = {
            'consumer_key': POCKET_CONSUMER_KEY,
            'redirect_uri': 'www.google.com'
        }
        r = get_pocket_request(POCKET_REQUEST, request_data)

        REQUEST_TOKEN.set_value(data, r['code'])
        set_user_data(data)

        auth_url = 'https://getpocket.com/auth/authorize?request_token={}&redirect_uri=www.google.com'.format(REQUEST_TOKEN.get_value(data))
        print('Please go to:')
        print(auth_url)
        print('and then run setup again')
    elif ACCESS_TOKEN.get_value(data) == '':
        print('Getting access token...')
        request_data = {
            'consumer_key': POCKET_CONSUMER_KEY,
            'code': REQUEST_TOKEN.get_value(data)
        }
        r = get_pocket_request(POCKET_AUTH, request_data)
        REQUEST_TOKEN.set_value(data, 'used')
        ACCESS_TOKEN.set_value(data, r['access_token'])
        USERNAME.set_value(data, r['username'])
        set_user_data(data)
        print('Setup done...')
    else:
        print('Setup done...')


def handle_debug(args):
    data = get_user_data()
    print('config file', get_config_file_name())
    print('cache file', get_cache_file_name())
    print('request', REQUEST_TOKEN.get_value(data))
    print('access', ACCESS_TOKEN.get_value(data))
    print('user', USERNAME.get_value(data))


def handle_list(args):
    data = get_all_pockets(args)
    data.sort(key=lambda pp: pp.added, reverse=args.reverse)
    for p in data:
        print(p.id)
        print(p.added)
        print(s(p.url))
        print(s(p.title))
        print(s(p.excerpt))
        print()


########################################################################################################################
# main function

def main():
    parser = argparse.ArgumentParser(description='Pocket CLI')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('setup', help='setup settings')
    sub.set_defaults(func=handle_setup)

    sub = sub_parsers.add_parser('debug', help='debug settings')
    sub.set_defaults(func=handle_debug)

    sub = sub_parsers.add_parser('list', help='init the project file')
    sub.add_argument('--filter', default='', help='url filter')
    sub.add_argument('--reverse', action='store_true', help='reverse list order')
    sub.set_defaults(func=handle_list)

    # todo(Gustav): mark for deletion, star and execute/push to pocket

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
