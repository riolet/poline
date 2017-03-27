# pol
pol lets you do awk-like one liners in python.

For example, the following will graph the number of connections for each hosts.
```bash
$ netstat -an | pol "map(print,['{}\t{}'.format(i['e'],'*' * i['c']) for i in sortedbycount([l[4].split(':')[0] for l in _ if len(l)>5 and l[5]=='ESTABLISHED'],True)])"
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

# Usage

```
pol [options] one-liner
Options
-F separator 		: Field Separator
```

# Quick Start
You can build and install pol from source as follows:

```
make
sudo make install
```


pol stores *stdin* in the variable *_* (underscore) in the form of a list of lists.

You can see what's inside *_* with:

```bash
$ ls -lah | pol "map(print,_)"
['total', '156K']
['drwxr-xr-x', '11', 'root', 'root', '4.0K', 'Aug', '2', '2016', '.']
['drwxr-xr-x', '25', 'root', 'root', '4.0K', 'Mar', '7', '16:17', '..']
['drwxr-xr-x', '2', 'root', 'root', '68K', 'Mar', '25', '13:44', 'bin']
['drwxr-xr-x', '2', 'root', 'root', '4.0K', 'Jul', '19', '2016', 'games']
['drwxr-xr-x', '69', 'root', 'root', '20K', 'Mar', '25', '13:44', 'include']
```

**N.B.** pol also imports *print_function*, so print can be used as a function.

# Utility Functions

We are in the process of adding utility functions to pol. Contributions are most welcome.

## sh (c, F=None)

Executes shell command specified in string c, and returns stdout in the form of a list of lists.

Example:

The following displays the inode of each file using *stat*

```
$ ls | pol "[print('{:10.10}\t{}'.format(l[0],[i[3] for i in sh('stat %s'%l[0]) if len(i)>2 and 'Inode:' in i[2]][0])) for l in _]"
LICENSE   	360621
Makefile  	360653
pol       	360606
pol.c     	360637
pol.o     	360599
README.md 	360623
```

## get (l, i, d = None)

get *i*th element from list *l* if the *i*th element exists, or return value d

```
>>> get([1, 2, 3, 4],1)
2
>>> get([1, 2, 3, 4],4,0)
0
```

## sortedbycount(l,reversed=False)

Sorts a list by assending order, and returns a list of dictionaries, in the form

```
[{e:<element1>,c:<count1>'},{e:<element2>,c:<count2>'},...,{e:<elementn>,c:<countn>'},
```

Example:

```
>>> sortedbycount(['i','n','f','o','r','m','a','t','i','o','n'],reverse=True)
[{'c': 2, 'e': 'i'}, {'c': 2, 'e': 'n'}, {'c': 2, 'e': 'o'}, {'c': 1, 'e': 'a'}, {'c': 1, 'e': 'f'}, {'c': 1, 'e': 'm'}, {'c': 1, 'e': 'r'}, {'c': 1, 'e': 't'}]
```


# Examples

#### The top ten commands you use most often
```
history | pol "map(print,['{}\t{}'.format(i['e'], i['c']) for i in sortedbycount([l[1] for l in _ if len(l)>1],True)][:10])"
```



