#!/usr/bin/python -tt

"""list all files in a given directory. Listing shows absolute path of files
   Usage: listfiles /path/directory"""

__author__ = "Daniel T."
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "danasmera"
__email__ = "daniel@danasmera.com"


import os
import sys
import signal

if len(sys.argv) > 1:
    mypath = sys.argv[1]
else:
    mypath = os.getcwd()


def main():
    """ main function """
    try:
        if os.path.exists(mypath) and os.path.isdir(mypath):
            for dp, dn, fn in os.walk(mypath):
                for myfile in fn:
                    print os.path.join(dp, myfile)
        else:
            print "mypath not found or not a directory!"
    except KeyboardInterrupt:
        print("Interrupt key pressed, aborting.")
        sys.exit(0)

if __name__ == "__main__":
    sys.exit(main())
