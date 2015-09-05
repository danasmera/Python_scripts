import sys
import itertools
from process import Process

class Scramble:

    def __init__(self, options):
        self.options = options
        self.process = Process()

    def date(self):
        self._get_date()

    def _get_date(self):
        print self.process.execute("date")

    def print_example_arg(self):
        print self.options.example

    def scramble(self):
       ''' Scramble core function '''
       var_scramble = self.options.example
       var_len = len(var_scramble)
       all_permuts = itertools.permutations(var_scramble,
                                            var_len)
       for item in list(set(all_permuts)):
           print '{0}'.format(''.join(item))
