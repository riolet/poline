#!/usr/bin/env bash

export PYTHONPATH=`pwd`
export PYTHONIOENCODING=UTF-8

virtualenv -p ${1} poline_venv
source poline_venv/bin/activate
${1} setup.py install

echo 'Test: repr(x) for x in _'
ls -lah | pol -s 'repr(x) for x in _'

echo "Test: '{}\t{}'.format(x,c) for x, c in counter(l[1] for l in _ if l[1])"
ls -lah | pol -s "'{}\t{}'.format(x,c) for x, c in counter(l[1] for l in _ if l[1])"

echo "Test: ls()"
pol "i[5] for i in ls('-lah',s=True)"

echo "Test: ls() with old syntax"
pol "i[5] for i in ls(['-lah'],s=True)"

echo "Test: df as bar graph"
df -B1 | pol -s "'{:10.10}\t{:10.10}\t{:10.10}\t{:10.10}\t{:5.5}\t{}{}\t{:10.10}'.format(i[0],bytesize(i[1]),bytesize(i[2]),bytesize(i[3]),i[4],'#'*int(10*int(i[2])/int(i[1])+0.5) if i[1].isdigit() else ' '*5, '_'*(10-int(10*int(i[2])/int(i[1])+0.5)) if i[1].isdigit() else ' '*5,i[5]) for i in _"

echo "Test: barchart function"
pol "'{:20.20}\t{:10.10}\t{:10.10}\t{:10.10}\t{:5.5}\t{}\t{:10.10}'.format(i[0],bytesize(i[1]),bytesize(i[2]),bytesize(i[3]),i[4], barchart(int(i[2])/float(i[1]),p=True) if i[1].isdigit() else ' '*10,i[5]) for i in df('-B1', s=T)"

echo "Test: columns function"
pol "columns(20,10,10,10,5,None,10).format(i[0],bytesize(i[1]),bytesize(i[2]),bytesize(i[3]),i[4], barchart(int(i[2])/float(i[1]),p=True) if i[1].isdigit() else ' '*10,i[5]) for i in df('-B1',s=T)"
