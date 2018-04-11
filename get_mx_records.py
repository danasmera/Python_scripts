#!/usr/bin/env python

'''Usage: scriptname domain
   Output will list of MX records of domain sorted by MX,
   lowest MX value first, and highest Mx value last.
   This script uses PriorityQueue Class and is based on
   Python Cookbook 3rd edition.
'''

__author__ = "Daniel T."
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "danasmera"
__email__ = "daniel@danasmera.com"

import os
import sys
import heapq


def Usage():
    print "{0} {1}".format(sys.argv[0], 'FQDN')
    sys.exit(1)

if len(sys.argv) != 2:
    Usage()

maildomain = sys.argv[1]
# Use dig command
mycommand = "dig +short " + maildomain + " mx"


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

q = PriorityQueue()


def push_mail_servers():
    counter = 0
    with os.popen(mycommand) as fp:
        for line in fp:
            mail_servers = line.strip()
            priority, mail_server = mail_servers.split()
            q.push(mail_server, int(priority))
            counter += 1
    return counter


def main():
    total_mx = push_mail_servers()
    while (total_mx > 0):
        print q.pop()
        total_mx -= 1

# Main
if __name__ == '__main__':
    sys.exit(main())

'''Usage example
[daniel@danasmera tmp]$ dig gmail.com mx +short
20 alt2.gmail-smtp-in.l.google.com.
30 alt3.gmail-smtp-in.l.google.com.
40 alt4.gmail-smtp-in.l.google.com.
5 gmail-smtp-in.l.google.com.
10 alt1.gmail-smtp-in.l.google.com.
[daniel@asmera tmp]$ ./get_mx_records.py gmail.com
gmail-smtp-in.l.google.com.
alt1.gmail-smtp-in.l.google.com.
alt2.gmail-smtp-in.l.google.com.
alt3.gmail-smtp-in.l.google.com.
alt4.gmail-smtp-in.l.google.com.
'''
