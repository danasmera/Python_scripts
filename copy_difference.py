#!/usr/bin/env python
'''Copy difference of two directories to a new directory. Finds newly added or modified files in a directory by comparing to an older directory, and copies those files/directories to a new difference directory recursively.
'''

import os, sys
import filecmp
import re
import shutil
#container for all newly added or modified files and directories
holderlist=[]

def compareme(dir1, dir2):
    dircomp=filecmp.dircmp(dir1,dir2)
    only_in_one=dircomp.left_only
    diff_in_one=dircomp.diff_files
    dirpath=os.path.abspath(dir1)
    [holderlist.append(os.path.abspath( os.path.join(dir1,x) )) for x in only_in_one]
    [holderlist.append(os.path.abspath( os.path.join(dir1,x) )) for x in diff_in_one]
    if len(dircomp.common_dirs) > 0:
        for item in dircomp.common_dirs:
            compareme(os.path.abspath(os.path.join(dir1,item)), os.path.abspath(os.path.join(dir2,item)))
        return holderlist

def main():
 if len(sys.argv) > 3:
   dir1=sys.argv[1]
   dir2=sys.argv[2]
   dir3=sys.argv[3]
 else:
   print "Usage: ", sys.argv[0], "currentdir olddir difference"
   sys.exit(1)
 if not os.path.isdir(dir1) or not os.path.isdir(dir2): 
   print "Supplied directory does not exist."
   sys.exit(1)
 if not dir3.endswith('/'): dir3=dir3+'/'

 source_files=compareme(dir1,dir2)
 dir1=os.path.abspath(dir1)
 dir3=os.path.abspath(dir3)
 destination_files=[]
 new_dirs_create=[]
 for item in source_files:
   destination_files.append(re.sub(dir1, dir3, item) )
 for item in destination_files:
  new_dirs_create.append(os.path.split(item)[0])
 for mydir in set(new_dirs_create):
   if not os.path.exists(mydir): os.makedirs(mydir)
#copy pair
 copy_pair=zip(source_files,destination_files)
 for item in copy_pair:
   if os.path.isfile(item[0]):
    shutil.copyfile(item[0], item[1])

if __name__ == '__main__':
 main()
