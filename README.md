# poline
poline lets you do awk-like one liners in python.

For example, the following will graph the number of connections for each hosts.

Python>=3.6
```bash
netstat -an | pol "f'''{x}\t{'*'*c}''' for x,c in counter(url(l[4]).hostname for l in _ if get(l,5)=='ESTABLISHED')" -s
```

Python>=3.0
```bash
netstat -an | pol "'''{}\t{}'''.format(x,'*'*c) for x,c in counter(url(l[4]).hostname for l in _ if get(l,5)=='ESTABLISHED')" -s
```
Example output:

```
216.58.193.78	    *****
74.125.199.189	    ****
198.252.206.25	    ***
74.125.199.188	    **
192.30.253.125	    **
127.0.0.1	    **
216.58.193.67	    *
```

The equivalent awk version can be found on [commandlinefu](http://www.commandlinefu.com/commands/view/2012/graph-of-connections-for-each-hosts).

# Installation

You can easily install poline is via pip:

```
pip3 install poline
```


# Usage

```
poline.py [-h] [-F SEPARATOR] [-s] expression

positional arguments:
  expression            python expression

optional arguments:
  -h, --help                            show this help message and exit
  -F SEPARATOR, --separator SEPARATOR   split each line by SEPARATOR
  -s, --split                           split each line

```

poline stores *stdin* in the variable *_* (underscore) in the form of a generator of lists.

You can see what's inside *_* with:

```bash
> ls -lah | pol "repr(x) for x in _" -s
['total', '156K']
['drwxr-xr-x', '11', 'root', 'root', '4.0K', 'Aug', '2', '2016', '.']
['drwxr-xr-x', '25', 'root', 'root', '4.0K', 'Mar', '7', '16:17', '..']
['drwxr-xr-x', '2', 'root', 'root', '68K', 'Mar', '25', '13:44', 'bin']
['drwxr-xr-x', '2', 'root', 'root', '4.0K', 'Jul', '19', '2016', 'games']
['drwxr-xr-x', '69', 'root', 'root', '20K', 'Mar', '25', '13:44', 'include']
```

# Utility Functions

We are in the process of adding utility functions to pol. Contributions are most welcome.

## sh (c, F=None)

Executes shell command specified in string c, and returns stdout in the form of a list of lists.

Example:

The following displays the inode of each file using *stat*

```
$ ls | pol "f'{l:10.10}\t%s' % [i[3] for i in sh(['stat',l]) if 'Inode:' in i[2]][0] for l in _" 
LICENSE   	360621
Makefile  	360653
pol       	360606
pol.c     	360637
pol.o     	360599
README.md 	360623
```

## get (l, i, d=None)

get *i*th element from list *l* if the *i*th element exists, or return value d

```python
>>> get([1, 2, 3, 4],1)
2
>>> get([1, 2, 3, 4],4,0)
0
```

## counter(l, n=10)

Sorts a list by descending order, and returns a 2-tuple with element and number of appearances in l:

```
[(<element>, <count>), ...]
```

Example:

```
$ pol "pprint(counter('information'), width=20)"
[('i', 2),
 ('n', 2),
 ('o', 2),
 ('f', 1),
 ('r', 1),
 ('m', 1),
 ('a', 1),
 ('t', 1)]
```

## bytesize(x)
Returns the number of bytes *x* in a human readable string with a 'B', 'K', 'M', 'G', 'T', 'P' prefix.

Example:

```
$ pol "bytesize(972693249)"
927.63 M
```


# Examples

#### The top ten commands you use most often
```
history | pol "f'{x}\t{c}' for x, c in counter(l[1] for l in _ if len(l) > 1)" -s
```
