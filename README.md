# pol
pol lets you do awk-like one liners in python.

For example, the following will graph the number of connections for each hosts.
```bash
$ netstat -an | pol "l=[l[4].split(':')[0] for l in _ if len(l)>5 and l[5]=='ESTABLISHED']; s=sorted([{'h':e,'c':l.count(e)} for e in set(l)],key=lambda k: k['c'], reverse=True); map(print,['{}\t{}'.format(i['h'],'*' * i['c']) for i in s])"
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

# Quick Start
pol gives you a list of list in the variable
```
_
```
Yes, that's the underscore.

pol also imports *print_function*, so print can be used as a function.

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










