import sys

from lib import Scramble
from lib import Options

''' This utility prints all combination of characters of input text '''

if __name__ == '__main__':
    options = Options()
    opts = options.parse(sys.argv[1:])

    v = Scramble(opts)
    v.date()
    v.print_example_arg()
    v.scramble()
