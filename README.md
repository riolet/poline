# poline

[![Build Status](https://jenkins-poline.hotbed.io/buildStatus/icon?job=poline-poline)](https://jenkins-poline.hotbed.io/job/poline-poline/)

poline lets you do awk-like one liners in python.

For example, the following will graph the number of connections for each hosts.

Python>=3.6
```bash
netstat -an | pol "f'''{x}\t{'*'*c}''' for x,c in counter(url(l[4]).hostname for l in _ if get(l,5)=='ESTABLISHED')" -s
```

Python>=2.7
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

poline is compatible with Python 2.7 to Python 3.6.

You can easily install poline is via pip:

```
pip install poline
```

or

```
pip<version> install poline
```

Where `<version>` is the version of python you wish to use. For example, if you want to use poline with Python 3.6 installed, you should use

```
pip3.6 install poline
```

# Usage

```
 pol [-h] [-F SEPARATOR] [-s] [-q] expression

positional arguments:
  expression            python expression

optional arguments:
  -h, --help            show this help message and exit
  -F SEPARATOR, --separator SEPARATOR
                        split each line by SEPARATOR
  -s, --split           split each line
  -q, --quiet           don't implicitly print results

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



## barchart(x, p = False, w = 10)

Returns the value *x* as a barchart. If *p* is true, x is intepreted as a percentage, with 100% being *w* wide.

```
$ df -B1 | pol -s "'{:20.20}\t{:10.10}\t{:10.10}\t{:10.10}\t{:5.5}\t{}\t{:10.10}'.format(i[0],bytesize(i[1]),bytesize(i[2]),bytesize(i[3]),i[4], barchart(int(i[2])/float(i[1]),p=True) if i[1].isdigit() else ' '*10,i[5]) for i in _"
Filesystem          	1B-blocks 	Used      	Available 	Use% 	          	Mounted
/dev/mapper/docker-8	  9.99 G  	  8.06 G  	  1.93 G  	81%  	▓▓▓▓▓▓▓▓░░	/
tmpfs               	 31.37 G  	  0.00 B  	 31.37 G  	0%   	░░░░░░░░░░	/dev
tmpfs               	 31.37 G  	  0.00 B  	 31.37 G  	0%   	░░░░░░░░░░	/sys/fs/cg
/dev/sda3           	211.08 G  	 26.49 G  	173.84 G  	14%  	▓░░░░░░░░░	/etc/hosts
shm                 	 64.00 M  	  0.00 B  	 64.00 M  	0%   	░░░░░░░░░░	/dev/shm

```

## bytesize(x, u = None, s = False)

Returns the number of bytes *x* in a human readable string with a 'B', 'K', 'M', 'G', 'T', 'P' prefix.

If x is a string, bytesize tries to convert it to a float, or returns the string as is.

*u* specifies that bytes are in a different unit, for example u='K' if the size is in 1-K blocks.

*s* specifies that byte size should be strict.

Example:

```
$ pol "bytesize(972693249)"
927.63 M
```

## counter(l, n=10)

Sorts a list by descending order, and returns a 2-tuple with element and number of appearances in l:

```
[(<element>, <count>), ...]
```

Example:

```
$ pol -q "pprint(counter('information'), width=20)"
[('i', 2),
 ('n', 2),
 ('o', 2),
 ('f', 1),
 ('r', 1),
 ('m', 1),
 ('a', 1),
 ('t', 1)]
```

## get (l, i, d=None)

get *i*th element from list *l* if the *i*th element exists, or return value d

```python
>>> get([1, 2, 3, 4],1)
2
>>> get([1, 2, 3, 4],4,0)
0
```


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

As well, the popular shell commands *cp*, *df*, *docker*, *du*, *find*, *git*, *history*, *ln*, *ls*, *lsof*, *mv*, *netstat*, *nmcli*, *ps*, *rm* are all functions. For example

They behave as if the command is being passed to *sh* above.

```
$ pol "ls(['-lah'])"
total 24K
drwxr-xr-x 7 default root  185 Mar 31 02:21 .
drwxrwxrwt 9 root    root  185 Mar 31 02:24 ..
drwxr-xr-x 8 default root  163 Mar 31 02:36 .git
-rw-r--r-- 1 default root  300 Mar 31 02:21 .gitignore
-rw-r--r-- 1 default root 1.1K Mar 31 02:21 LICENSE
-rw-r--r-- 1 default root 3.5K Mar 31 02:21 README.md
```

# Examples

#### The top ten commands you use most often
```
history | pol "f'{x}\t{c}' for x, c in counter(l[1] for l in _ if len(l) > 1)" -s
```

