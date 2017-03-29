#!/usr/bin/env bash

ls -lah | PYTHONPATH=`pwd` $1 poline/poline.py -s 'repr(x) for x in _'
ls -lah | PYTHONPATH=`pwd` $1 poline/poline.py -s "'{}\t{}'.format(x,c) for x, c in counter(l[1] for l in _ if l[1])"
PYTHONPATH=`pwd` $1 poline/poline.py "i[5] for i in netstat('-tulpn',s=True)"