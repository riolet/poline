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
    sys.stdin.close()

# Hello old friends
_shell_commands= ['cp', 'df', 'docker', 'du', 'find', 'grep', 'git', 'history',
                  'ln', 'ls', 'lsof', 'mv', 'netstat', 'nmcli', 'ps', 'rm',
                  'stat', 'whois']

for _shell_command in _shell_commands:
    exec ("""{funcname} = lambda *args, **kwargs: sh(['{funcname}']+list(args), **kwargs)""".format(funcname=_shell_command))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', nargs='+', help="python expression")
    parser.add_argument('-F', '--separator', default=None, help="split each line by SEPARATOR")
    parser.add_argument('-s', '--split', const=True, default=False, action='store_const', help="split each line")
    parser.add_argument('-q', '--quiet', const=True, default=False, action='store_const',
                        help="don't implicitly print results")

    if argv is not None:
        args = parser.parse_args(argv)
    else:
        args = parser.parse_args()

    result = _stdin(args)

    for expression in args.expression:
        separator = None
        new_result = []
        if expression.startswith('|') or expression.startswith('%'):
            if expression.startswith('%'):
                expression = expression[1:]
                exp_parts = expression.split('%')
                separator = exp_parts[0]
                expression = '%'.join(exp_parts[1:])
            else:
                expression = expression[1:]

            for result_line in result:

                if separator:
                    result_parts = Fields(result_line.split(separator))
                else:
                    result_parts = Fields(result_line.split())

                invars = {
                    '_': result,
                    '__': result_parts,
                    '__str': result_line,
                    'len': _len,
                }

                for result_pard_idx in range(len(result_parts)+10):
                    invars['_{}'.format(result_pard_idx)] = result_parts[result_pard_idx]

                new_result += [eval('(%s)' % expression, globals(), invars)]
            result = new_result

        elif expression.startswith(':'):
            invars = {
                '_': result,
                'len': _len,
            }
            expression = expression[1:]
            exp_parts = expression.split(':')
            tuples = exp_parts[0]
            expression = '{} {}'.format(':'.join(exp_parts[1:]), 'for ({}) in _'.format(tuples))
            result = eval('(%s)' % expression, globals(), invars)

        else:
            invars = {
                    '_': result,
                    'len': _len,
            }
            result = eval('(%s)' % expression, globals(), invars)


    #argv is not None when we're calling this from a unit test
    if argv is not None:
        return result

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
