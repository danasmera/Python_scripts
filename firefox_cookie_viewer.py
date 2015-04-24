#!/usr/bin/env python
 
''' Given a location to firefox cookie sqlite file
    Write its date param - expiry, last accessed,
    Creation time to a file in plain text.
    id
    baseDomain
    appId
    inBrowserElement
    name
    value
    host
    path
    expiry
    lastAccessed
    creationTime
    isSecure
    isHttpOnly
    python /home/daniel/python/cookie_viewer.py $(find /home/daniel/ -type f -name 'cookies.sqlite' | head -1) /tmp/test.txt 
'''
 
__author__ = "Daniel T."
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "danasmera"
__email__ = "daniel@danasmera.com"

import sys
import os
from datetime import datetime
import sqlite3
 
def Usage():
    print "{0} cookie-fullpath output-file".format(sys.argv[0])
    sys.exit(1)
 
if len(sys.argv)<3:
    Usage()
 
sqldb=sys.argv[1]
destfile=sys.argv[2]
# Some dates in the cookies file might not be valid, or too big
MAXDATE=2049840000
 
# cookies file must be there, most often file name is cookies.sqlite
if not os.path.isfile(sqldb):
    Usage()
 
# a hack - to convert the epoch times to human readable format
def convert(epoch):
    mydate=epoch[:10]
    if int(mydate)>MAXDATE:
        mydate=str(MAXDATE)
    if len(epoch)>10:
        mytime=epoch[11:]
    else:
        mytime='0'
    fulldate=float(mydate+'.'+mytime)
    x=datetime.fromtimestamp(fulldate)
    return x.ctime()
 
# Bind to the sqlite db and execute sql statements
conn=sqlite3.connect(sqldb)
cur=conn.cursor()
try:
    data=cur.execute('select * from moz_cookies')
except sqlite3.Error, e:
    print 'Error {0}:'.format(e.args[0])
    sys.exit(1)
mydata=data.fetchall()
 
# Dump results to a file
with open(destfile, 'w') as fp:
    for item in mydata:
        urlname=item[1]
        urlname=item[1]
        expiry=convert(str(item[8]))
        accessed=convert(str(item[9]))
        created=convert(str(item[10]))
        fp.writelines(urlname + ',' + expiry + ',' + accessed + ',' + created)
        fp.writelines('\n')
 
# Dump to stdout as well
with open(destfile) as fp:
    for line in fp:
        print line
