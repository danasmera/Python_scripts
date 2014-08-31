#!/usr/bin/env python

import sys
from random import choice
import re
import signal

try:
  import dns.name
  import dns.message
  import dns.query
except ImportError:
  print 'Module dns import error.'
  sys.exit(1)

def signal_handler(signal, frame):
  print 'Ctrl+C pressed...exiting...'
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def Usage():
  print sys.argv[0] + ' FQDN RecordType[A|MX|TXT|NS|ANY]'
  print "Ex. " + sys.argv[0] + ' gmail.com mx'
  sys.exit(1)

mydict={'A':1 ,'NS':2,'MX':15,'TXT':16,'ANY':255}

ARGC=len(sys.argv)

if ARGC < 2:
  Usage()

RRTYPE='A' if ARGC<=2 else sys.argv[2].strip()
RRTYPE=RRTYPE.upper()
if RRTYPE in mydict: RRTYPE=mydict[RRTYPE]   
else: sys.exit(1)

#IPv4 pattern
ippat=r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}'

#rootns=[chr(i)+'.root-servers.net' for i in range(ord('a'),ord('n'))]
rootns=( '198.41.0.4' , '192.228.79.201' , '192.33.4.12' , '199.7.91.13' , '192.203.230.10' , '192.5.5.241' , '192.112.36.4' , '128.63.2.53' , '192.36.148.20' ,'192.58.128.30' , '193.0.14.129' , '199.7.83.42' , '202.12.27.33' ) 

srootns=choice(rootns)

print "Selected root name server: " , srootns

def only_ip(rrdata):
  match=re.search(ippat, rrdata)
  if match: return match.group()

#we will accept input such as google.com www.google.com. etc
myhost=sys.argv[1]
cleaned_myhost=myhost.split('.')
if not cleaned_myhost[-1].endswith('.'):
  cleaned_myhost.extend('.')

#flip list into format ['.','com','google' ,'www' ]
cleaned_myhost.reverse()
if '' in cleaned_myhost: cleaned_myhost.remove('')

#Split into parts in reverse for easier querying ['.','com.', 'google.com.', www.google.com.']
i=1
while i < len(cleaned_myhost):
   if i==1: 
     cleaned_myhost[i]=cleaned_myhost[i]+cleaned_myhost[i-1]
   else:
     cleaned_myhost[i]=cleaned_myhost[i]+'.'+cleaned_myhost[i-1]
   i+=1

print cleaned_myhost
additional_ns=[]


##Step over reach domain part and query the NS in the glue record on parent domain

for domain in cleaned_myhost[1:]:
  name_server=srootns
  ndomain = dns.name.from_text(domain)
  request = dns.message.make_query(ndomain, dns.rdatatype.NS)
  if additional_ns : name_server=choice(additional_ns)
  try:
    response = dns.query.udp(request, name_server, timeout=10)
  except dns.exception.Timeout:
    print 'Dns query timed out.'
    sys.exit(1)

  additional_ns=[]
  #Skip IPv6
  for item in response.additional:
    if not 'IN AAAA' in item.to_text():
      ip_ns=only_ip(item.to_text())
      if ip_ns: additional_ns.append(only_ip(ip_ns))
 # name_server=choice(additional_ns)
  if additional_ns: 
    LNS=choice(additional_ns)
    print "Random NS: ", LNS

print
print "Querying name server: ", LNS
#request = dns.message.make_query(myhost, dns.rdatatype.A)
request = dns.message.make_query(myhost, int(RRTYPE))
try:
  response = dns.query.udp(request, LNS, timeout=10)
except dns.exception.Timeout:
  print 'Dns query timed out.'
  sys.exit(1)

for rrset in response.answer:
  print rrset
