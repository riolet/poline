#!/usr/bin/env bash

echo 'Test: repr(x) for x in _'
ls -lah | PYTHONPATH=`pwd` $1 poline/poline.py -s 'repr(x) for x in _'

echo "Test: '{}\t{}'.format(x,c) for x, c in counter(l[1] for l in _ if l[1])"
ls -lah | PYTHONPATH=`pwd` $1 poline/poline.py -s "'{}\t{}'.format(x,c) for x, c in counter(l[1] for l in _ if l[1])"

echo "Test: i[5] for i in netstat('-tulpn',s=True)"
PYTHONPATH=`pwd` $1 poline/poline.py "i[5] for i in ls('-lah',s=True)"

echo "Test: df as bar graph"
df -B1 | PYTHONPATH=`pwd` $1 poline/poline.py -s "'{:10.10}\t{:10.10}\t{:10.10}\t{:10.10}\t{:5.5}\t{}{}\t{:10.10}'.format(i[0],bytesize(i[1],f=True),bytesize(i[2],f=True),bytesize(i[3],f=True),i[4],'#'*int(10*int(i[2])/int(i[1])+0.5) if i[1].isdigit() else ' '*5, '_'*(10-int(10*int(i[2])/int(i[1])+0.5)) if i[1].isdigit() else ' '*5,i[5]) for i in _"
