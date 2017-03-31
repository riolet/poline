#!/usr/bin/env bash

export PYTHONPATH=`pwd`
export PYTHONIOENCODING=UTF-8

export testpol="${1} poline/poline.py"

echo 'Test: repr(x) for x in _'
ls -lah | ${testpol} -s 'repr(x) for x in _'

echo "Test: '{}\t{}'.format(x,c) for x, c in counter(l[1] for l in _ if l[1])"
ls -lah | ${testpol} -s "'{}\t{}'.format(x,c) for x, c in counter(l[1] for l in _ if l[1])"

echo "Test: ls()"
${testpol} "i[5] for i in ls('-lah',s=True)"

echo "Test: ls() with old syntax"
${testpol} "i[5] for i in ls(['-lah'],s=True)"

echo "Test: df as bar graph"
df -B1 | ${testpol} -s "'{:10.10}\t{:10.10}\t{:10.10}\t{:10.10}\t{:5.5}\t{}{}\t{:10.10}'.format(i[0],bytesize(i[1],f=True),bytesize(i[2],f=True),bytesize(i[3],f=True),i[4],'#'*int(10*int(i[2])/int(i[1])+0.5) if i[1].isdigit() else ' '*5, '_'*(10-int(10*int(i[2])/int(i[1])+0.5)) if i[1].isdigit() else ' '*5,i[5]) for i in _"

echo "Test: barchart function"
df -B1 | ${testpol} -s "'{:20.20}\t{:10.10}\t{:10.10}\t{:10.10}\t{:5.5}\t{}\t{:10.10}'.format(i[0],bytesize(i[1]),bytesize(i[2]),bytesize(i[3]),i[4], barchart(int(i[2])/float(i[1]),p=True) if i[1].isdigit() else ' '*10,i[5]) for i in _"
