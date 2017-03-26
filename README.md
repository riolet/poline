# pol
pol lets you do awk-like one liners in python.

For example, the following will graph the number of connections for each hosts.
```
netstat -an | pol "l=[l[4].split(':')[0] for l in _ if len(l)>5 and l[5]=='ESTABLISHED']; s=sorted([{'h':e,'c':l.count(e)} for e in set(l)],key=lambda k: k['c'], reverse=True); map(print,['{}\t{}'.format(i['h'],'*' * i['c']) for i in s])"
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
