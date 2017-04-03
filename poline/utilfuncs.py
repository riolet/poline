from __future__ import print_function

import re
import sys
import collections
import subprocess
from poline.fields import Fields

if sys.version_info >= (3,0):
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

if sys.version_info >= (3,5):
    _collections_Generator = collections.Generator
else:
    from poline import _com_collections
    _collections_Generator = _com_collections.Generator

def url(url):
    if not re.match('([a-z]+:)?//', url):
        url = '//' + url
    return urlparse(url)


def counter(l, n=10):
    return collections.Counter(l).most_common(n)


def sh(*args, **kwargs):
    if isinstance(args[0],list):
        cmd = args[0]
    else:
        cmd = list (args)
    shell = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for stdout in shell.stdout:
        if 'F' in kwargs:
            yield Fields(stdout.strip().decode().split(kwargs['F']))
        elif 's' in kwargs and kwargs['s']:
            yield Fields(stdout.strip().decode().split())
        else:
            yield stdout.strip().decode()
    for stderr in shell.stderr:
        print(stderr.strip().decode(), file=sys.stderr)


def skip(iterable, n=1):
    for n in range(n):
        next(iterable)
    return iterable


def get(l, i, d=None):
    if isinstance(l, _collections_Generator):
        for j, v in enumerate(l):
            if i == j:
                return v
        return d
    else:
        return l[i] if len(l) > i else d


def bytesize(x, u = None, s = False):
    #Check if we're running ignore non-digits mode
    if not s:
        if not x.isdigit():
            return x
        else:
            x=float(x)

    units = ['P', 'T', 'G', 'M', 'K', 'B']
    offset = 0
    if u is not None and units.index(u) > 0:
        offset = len(units)-units.index(u) - 1
    for i in range(len(units)):
        if x == 0:
            return '{:6.2f} {}'.format(0,units[-1])
        if x // 1024**(len(units) - i - 1 - offset) > 0:
            return '{:6.2f} {}'.format(x / float(1024**(len(units) - i - 1 - offset)), units[i])

def barchart(x, p = False, w = 10):
    if sys.version_info >= (3, 0):
        d = '\N{DARK SHADE}'
        l = '\N{LIGHT SHADE}'
    else:
        d = u'\u2593'.encode('utf-8')
        l = u'\u2591'.encode('utf-8')
    if p:
        x = int(round (x * w))
        return d*x + l*(w-x)
    else:
        return d*x


class Cols:
    def gen_n_columns(self,n):
        for i in range(n):
            if len(self.fmtstr) > 0:
                self.fmtstr += "\t"
            self.fmtstr += "{}"

    def __init__(self, *args, **kwargs):
        self.fmtstr = ""
        if 'n' in kwargs:
            self.gen_n_columns(kwargs['n'])
        else:
            for f in args:
                if len(self.fmtstr) > 0:
                    self.fmtstr += "\t"
                if f is None:
                    self.fmtstr += "{}"
                elif isinstance(f, int):
                    self.fmtstr += "{:%d.%d}" % (f, f)
                elif isinstance(f, int):
                    self.fmtstr += "{:%f}" % (f)
                else:
                    fstr = '{}'.format(f)
                    self.fmtstr += "{%s}" % fstr

    def f(self, *args):
        if self.fmtstr == "":
            self.gen_n_columns(len(args))
        return self.fmtstr.format(*args)