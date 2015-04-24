#!/usr/bin/env python
'''extract a list of URLs from Firefox exported bookmars JSON file '''
 
__author__ = "Daniel T."
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "danasmera"
__email__ = "daniel@danasmera.com"

import sys
import os
import json
import io

def Usage():
    print "{0} Path-to-bookmarks-file".format(sys.argv[0])
    sys.exit(1)

if len(sys.argv) < 2:
    Usage()

bookmark_file = sys.argv[1]

#Does the file exist?
if not os.path.isfile(bookmark_file):
    print "{0} not found.".format(bookmark_file)
    sys.exit(1)

# Load JSON file 
fp_data = io.open(bookmark_file, encoding='utf-8')
try:
    jdata = json.load(fp_data)
except ValueError:
    print "{0} not valid JSON file".format(bookmark_file)
    sys.exit(1)
fp_data.close()
 
 
#Recursive function to get the title and URL keys from JSON file
 
def grab_keys(bookmarks_data, bookmarks_list=[]):
  if 'children' in bookmarks_data:
    for item in bookmarks_data['children']:
      bookmarks_list.append({'title': item.get('title', 'No title'),
                             'uri': item.get('uri', 'None')})
      grab_keys(item, bookmarks_list)
  return bookmarks_list
 
 
def main():
  mydata=grab_keys(jdata)
  for item in mydata:
    myurl = item['uri']
    if myurl.startswith('http') or myurl.startswith('ftp'):
      print item['uri'], "  ", item['title']
 
if __name__=="__main__":
  main()
