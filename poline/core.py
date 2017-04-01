from __future__ import print_function

import re
import os
import sys
import argparse
import collections
import subprocess
import json
from poline.utilfuncs import *
from poline.fields import Fields

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
    from poline import _com_collections
    _collections_Generator = _com_collections.Generator


T = True
F = False

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

# Hello old friends
_shell_commands= ['cp', 'df', 'docker', 'du', 'find', 'git', 'history',
                  'ln', 'ls', 'lsof', 'mv', 'netstat', 'nmcli', 'ps', 'rm']
for _shell_command in _shell_commands:
    exec ("""{funcname} = lambda *args, **kwargs: sh(['{funcname}']+list(args), **kwargs)""".format(funcname=_shell_command))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', help="python expression")
    parser.add_argument('-F', '--separator', default=None, help="split each line by SEPARATOR")
    parser.add_argument('-s', '--split', const=True, default=False, action='store_const', help="split each line")
    parser.add_argument('-q', '--quiet', const=True, default=False, action='store_const',
                        help="don't implicitly print results")

    if argv is not None:
        args = parser.parse_args(argv)
    else:
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
