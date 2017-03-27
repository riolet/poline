# Hall of Fame

### Submit your one-liner

Please submit a PR with your one-liner to add it to the Hall of Fame.

#### Graph the number of connections for IP address for your box, and to whom the IP address belongs to

```bash
netstat -an | pol "map(print,['{}\t{:25.25}\t{}'.format(i['e'],get([' '.join(l[1:]) for l in sh('whois %s'%i['e']) if len(l)>0 and 'OrgName' in l[0]],0),'*' * i['c']) for i in sortedbycount([l[4].split(':')[0] for l in _ if len(l)>5 and l[5]=='ESTABLISHED'],True)[:10]])"
```

Example return value

```
127.0.0.1	    Internet Assigned Numbers	**************
216.58.193.78	    Google Inc.              	********
198.252.206.25	    Stack Exchange, Inc.     	*****
192.30.253.124	    GitHub, Inc.             	****
74.125.199.188	    Google Inc.              	**
74.125.199.189	    Google Inc.              	**
151.101.53.140	    Fastly                   	*
```

