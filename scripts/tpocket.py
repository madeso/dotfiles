#!/usr/bin/env python3
import argparse
import json
import typing
import os
import datetime
import urllib.request
import urllib.parse
import urllib.error
import collections

########################################################################################################################
# Common functions

def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def get_home_folder() -> str:
    return os.path.expanduser('~')


def get_config_file_name() -> str:
    return os.path.join(get_home_folder(), '.tpocket.json')


class Data:
    def __init__(self, data: typing.Dict[str, str]):
        self.data = data


def get_user_data() -> Data:
    if file_exist(get_config_file_name()):
        with open(get_config_file_name(), 'r', encoding="utf-8") as f:
            return Data(json.loads(f.read()))
    else:
        return Data({})


def set_user_data(data: Data):
    with open(get_config_file_name(), 'w', encoding="utf-8") as f:
        print(json.dumps(data.data, sort_keys=True, indent=4), file=f)


class Settings:
    def __init__(self, name, default_value):
        self.name = name
        self.default_value = default_value

    def get_value(self, data:Data):
        if self.name not in data.data:
            return self.default_value
        else:
            return data.data[self.name]

    def set_value(self, data: Data, value):
        data.data[self.name] = value

    def set_defualt_if_missing(self, data: Data):
        if self.name not in data.data:
            data.data[self.name] = self.default_value


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
DELETE_LIST = Settings('delete_list', [])

########################################################################################################################
# Pocket functions

# reference: https://getpocket.com/developer/docs/v3/retrieve

POCKET_CONSUMER_KEY = '88378-7e4d291dcf51de39675f5caa'
POCKET_REQUEST = 'https://getpocket.com/v3/oauth/request'
POCKET_AUTH = 'https://getpocket.com/v3/oauth/authorize'
POCKET_GET = 'https://getpocket.com/v3/get'
POCKET_SEND = 'https://getpocket.com/v3/send'


def get_pocket_request(url, data):
    the_method = 'GET' if data is None else 'POST'
    r = urllib.request.Request(url=url, method=the_method)
    if data is not None:
        r.add_header('Content-Type', 'application/json; charset=UTF8')

    r.add_header('X-Accept', 'application/json')
    data_encoded = json.dumps(data).encode('utf-8') if data is not None else None
    with urllib.request.urlopen(r, data=data_encoded) as f:
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


def get_all_pockets_data(refresh: bool):
    data = get_user_data()

    if ACCESS_TOKEN.get_value(data) == '':
        return []
    if not refresh and file_exist(get_cache_file_name()):
        # todo(Gustav): check for latest if enought time has passed
        with open(get_cache_file_name(), 'r', encoding="utf-8") as f:
            return json.loads(f.read())
    else:
        print('Downloading posts from pocket...')
        request_data = {
            'consumer_key': POCKET_CONSUMER_KEY,
            'access_token': ACCESS_TOKEN.get_value(data)
        }
        gets = get_pocket_request(POCKET_GET, request_data)
        with open(get_cache_file_name(), 'w', encoding="utf-8") as f:
            print(json.dumps(gets, sort_keys=True, indent=4), file=f)
        return gets


def set_all_pockets_data(data):
    with open(get_cache_file_name(), 'w', encoding="utf-8") as f:
        print(json.dumps(data, sort_keys=True, indent=4), file=f)


def pocket_data_remove_post(data, post_id):
    posts = data['list']
    posts.pop(post_id)
    return data


def get_all_pockets(args, refresh=False) -> typing.List[Post]:
    data = get_all_pockets_data(refresh)
    ret = []
    for postid, post in data['list'].items():
        add = True
        post = Post(postid, post)

        if args.filter != '' and args.filter not in post.url:
            add = False

        if add:
            ret.append(post)

    return ret


def get_all_add_subargs(sub):
    sub.add_argument('--filter', default='', help='url filter')


def mark_for_delete(data: Data, p: Post):
    dl: typing.List[int] = DELETE_LIST.get_value(data)
    dl.append(p.id)
    DELETE_LIST.set_value(data, dl)
    print('Deleting id ', p.id)


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


def handle_refresh(args):
    args.filter = ''
    data = get_all_pockets(args, refresh=True)


def handle_list(args):
    data = get_all_pockets(args)
    data.sort(key=lambda pp: pp.added, reverse=args.reverse)
    for p in data:
        if args.display_id:
            print(p.id)
        if args.display_date:
            print(p.added)
        if args.display_url:
            print(s(p.url))
        if args.display_title:
            print(s(p.title))
        if args.display_excerpt:
            print(s(p.excerpt))
        if not args.compact:
            print()
        # pehaps add support for?
        # https://pypi.org/project/breadability/
        # https://github.com/codelucas/newspaper


def handle_host(args):
    data = get_all_pockets(args)
    counter = collections.Counter(urllib.parse.urlparse(p.url).hostname for p in data)
    items = sorted(counter.items(), key=lambda x: x[1]) if args.all else counter.most_common(args.top)
    for host, count in items:
        print('  ', host, count)


def handle_delete(args):
    data = get_user_data()
    pockets = get_all_pockets(args)
    delete_all = False
    for p in pockets:
        if delete_all:
            mark_for_delete(data, p)
        else:
            if args.range > 0:
                for x in range(args.range):
                    print()

            if p.id in DELETE_LIST.get_value(data):
                continue

            print('Delete?')
            if args.display_title:
                print('title:', s(p.title))
            if args.display_url:
                print('url:  ', s(p.url))
            if args.display_date:
                print(p.added)
            if args.display_excerpt:
                print(s(p.excerpt))
            while True:
                i = input('d(delete)/A(ll)/n(ext)/a(bort) > ')
                if i == 'd':
                    mark_for_delete(data, p)
                    break
                elif i == 'a':
                    print('aborting...')
                    set_user_data(data)
                    return
                elif i == 'A':
                    delete_all = True
                    mark_for_delete(data, p)
                    break
                elif i == 'n':
                    break
                else:
                    print('Unknown option ', i)
    set_user_data(data)


def handle_pending(args):
    data = get_user_data()
    pockets = {p.id: p for p in get_all_pockets(args)}

    if args.clear:
        DELETE_LIST.set_value(data, [])
        set_user_data(data)

    for id in DELETE_LIST.get_value(data):
        if id in pockets:
            p = pockets[id]
            print(s(p.title))
        else:
            print('ERROR: missing id:', id)


def handle_push(args):
    data = get_user_data()
    delete_list = DELETE_LIST.get_value(data)
    if len(delete_list) <= 0:
        print('No things to delete, aborting...')
        return

    if ACCESS_TOKEN.get_value(data) == '':
        print('Not logged in to pocket, aborting...')
        return

    to_send = []
    for post_id in delete_list:
        to_send.append({'action': 'delete', 'item_id': post_id})

    request_data = {
        'actions': json.dumps(to_send, sort_keys=True),
        'access_token': ACCESS_TOKEN.get_value(data),
        'consumer_key': POCKET_CONSUMER_KEY
    }
    arg = urllib.parse.urlencode(request_data)
    url = '{}?{}'.format(POCKET_SEND, arg)
    delete_result = get_pocket_request(url, None)['action_results']

    pocket_data = get_all_pockets_data(refresh=False)

    new_list = []
    removed_count = 0
    for post_id, removed in zip(delete_list, delete_result):
        if removed:
            pocket_data_remove_post(pocket_data, post_id)
            removed_count += 1
        else:
            new_list.append(post_id)

    DELETE_LIST.set_value(data, new_list)

    set_user_data(data)
    set_all_pockets_data(pocket_data)
    print('{} removed of {} total. {} remaining.'.format(removed_count, len(delete_list), len(new_list)))


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
    get_all_add_subargs(sub)
    sub.add_argument('--reverse', action='store_true', help='reverse list order')
    sub.add_argument('--id', dest='display_id', action='store_true', help="display post id")
    sub.add_argument('--url', dest='display_url', action='store_true', help="display post url")
    sub.add_argument('--no-date', dest='display_date', action='store_false', help="don't display date")
    sub.add_argument('--no-title', dest='display_title', action='store_false', help="don't display title")
    sub.add_argument('--no-excerpt', dest='display_excerpt', action='store_false', help="don't display excerpt")
    sub.add_argument('--compact', action='store_true', help="compact display")
    sub.set_defaults(func=handle_list)

    sub = sub_parsers.add_parser('hosts', help='list all hosts')
    get_all_add_subargs(sub)
    sub.add_argument('--top', type=int, default=10, help='the number of items to display')
    sub.add_argument('--all', action='store_true', help='ignore top arg, display all')
    sub.set_defaults(func=handle_host)

    sub = sub_parsers.add_parser('delete', help='delete posts')
    get_all_add_subargs(sub)
    sub.add_argument('--range', type=int, default=3, help='number of newlines between each promp')
    sub.add_argument('--url', dest='display_url', action='store_true', help="display post url")
    sub.add_argument('--no-date', dest='display_date', action='store_false', help="don't display date")
    sub.add_argument('--no-title', dest='display_title', action='store_false', help="don't display title")
    sub.add_argument('--no-excerpt', dest='display_excerpt', action='store_false', help="don't display excerpt")
    sub.set_defaults(func=handle_delete)

    sub = sub_parsers.add_parser('pending', help='list outgoing changes')
    get_all_add_subargs(sub)
    sub.add_argument('--clear', action='store_true', help="clear pending first")
    sub.set_defaults(func=handle_pending)

    sub = sub_parsers.add_parser('push', help='send pending changes to pocket')
    sub.set_defaults(func=handle_push)

    sub = sub_parsers.add_parser('refresh', help='refresh cached data')
    sub.set_defaults(func=handle_refresh)

    # todo(Gustav): star and execute/push to pocket

    args = parser.parse_args()
    if args.command_name is not None:
        try:
            args.func(args)
        except urllib.error.HTTPError as x:
            print(x)
            err = 'X-Error'
            if err in x.headers:
                print(x.headers[err])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
