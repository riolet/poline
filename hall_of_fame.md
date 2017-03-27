# Hall of Fame

### Submit your one-liner

Please submit a PR with your one-liner to add it to the Hall of Fame.

#### Graph the number of connections for IP address for your box, and to whom the IP address belongs to

```bash
netstat -an | pol "map(print,['{}\t{:25.25}\t{}'.format(i['e'],get([' '.join(l[1:]) for l in sh('whois %s'%i['e']) if len(l)>0 and 'OrgName' in l[0]],0),'*' * i['c']) for i in sortedbycount([l[4].split(':')[0] for l in _ if len(l)>5 and l[5]=='ESTABLISHED'],True)[:10]])"
```

Example output

```
127.0.0.1	    Internet Assigned Numbers	**************
216.58.193.78	    Google Inc.              	********
198.252.206.25	    Stack Exchange, Inc.     	*****
192.30.253.124	    GitHub, Inc.             	****
74.125.199.188	    Google Inc.              	**
74.125.199.189	    Google Inc.              	**
151.101.53.140	    Fastly                   	*
```


#### The top ten commands you use most often
```
history | pol "map(print,['{}\t{}'.format(i['e'], i['c']) for i in sortedbycount([l[1] for l in _ if len(l)>1],True)][:10])"
```

Example output

```
netstat	246
ps	176
ls	154
sudo	95
git	60
find	44
cat	39
history	37
pol	20
gcc	18
```

#### The list of largest open files

```
lsof / | pol "[print('{}\t{}\t{}'.format(bytesize(x[2]),x[0],x[1])) for x in sorted(set([(l[0],get(l,8),int(l[6])) for l in _[1:]]),key=lambda x:x[2],reverse=True)[:10]]"
```

Example output

```
107.76 M	chrome	/opt/google/chrome/chrome
  90.77 M	java	/opt/pycharm-community-2016.2/lib/pycharm.jar
  61.72 M	java	/opt/installs/pycharm-community-2016.2/jre/jre/lib/rt.jar
  35.66 M	skype	/usr/lib/i386-linux-gnu/libQtWebKit.so.4.10.2
  34.21 M	skype	/usr/bin/skype
  27.73 M	chrome	/usr/lib/nvidia-375/libnvidia-glcore.so.375.39
  24.71 M	xfwm4	/usr/lib/x86_64-linux-gnu/libicudata.so.55.1
  24.71 M	mousepad	/usr/lib/x86_64-linux-gnu/libicudata.so.55.1
  24.71 M	php	/usr/lib/x86_64-linux-gnu/libicudata.so.55.1
  24.71 M	gimp-2.8	/usr/lib/x86_64-linux-gnu/libicudata.so.55.1
```