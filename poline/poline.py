from __future__ import print_function

import re
import os
import sys
import argparse
import collections
import subprocess
import json

from itertools import islice
from operator import itemgetter, attrgetter
if sys.version_info >= (3,0):
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

from pprint import pprint, pformat

if sys.version_info >= (3,5):
    _collections_Generator = collections.Generator
else:
    from _compatibility import _com_collections
    _collections_Generator = _com_collections.Generator

class Fields(list):

    def __getitem__(self, i):
        if isinstance(i, int):
            if sys.version_info >= (3, 0):
                return super().__getitem__(i) if len(self) > i else ''
            else:
                return super(Fields, self).__getitem__(i) if len(self) > i else ''
        else:
            if sys.version_info >= (3, 0):
                return super().__getitem__(i)
            else:
                return super(Fields, self).__getitem__(i)

def url(url):
    if not re.match('([a-z]+:)?//', url):
        url = '//' + url
    return urlparse(url)


def counter(l, n=10):
    return collections.Counter(l).most_common(n)


def sh(c, F=None):
    lines = subprocess.check_output(c).decode().splitlines()
    return [Fields(line.strip().split(F)) for line in lines]


def get(l, i, d=None):
    if isinstance(l, _collections_Generator):
        for j, v in enumerate(l):
            if i == j:
                return v
        return d
    else:
        return l[i] if len(l) > i else d


def bytesize(x):
    units = ['P', 'T', 'G', 'M', 'K', 'B']
    for i in range(len(units)):
        if x == 0:
            return '{:6.2f} {}'.format(0,units[-1])
        if x // 1024**(len(units) - i - 1) > 0:
            return '{:6.2f} {}'.format(x / (1024**(len(units) - i - 1)), units[i])


def _len(value):
    if isinstance(value, _collections_Generator):
        return sum(1 for x in value)
    else:
        return len(value)


def _stdin(args):
    for line in sys.stdin:
        if args.separator is not None:
            yield Fields(line.strip().split(args.separator))
        elif args.split:
            yield Fields(line.strip().split())
        else:
            yield line.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', help="python expression")
    parser.add_argument('-F', '--separator', default=None, help="split each line by SEPARATOR")
    parser.add_argument('-s', '--split', const=True, default=False, action='store_const', help="split each line")
    parser.add_argument('-q', '--quiet', const=True, default=False, action='store_const',
                        help="don't implicitly print results")
    args = parser.parse_args()

    result = eval('(%s)' % args.expression, globals(), {
        '_': _stdin(args),
        'len': _len,
    })

    if not args.quiet:
        if isinstance(result, (list, _collections_Generator)):
            for line in result:
                if isinstance(line, (list, tuple)):
                    print(*line)
                else:
                    print(line)
        else:
            print(result)


if __name__ == "__main__":
    main()
