from argparse import ArgumentParser


class Options:

    def __init__(self):
        self._init_parser()

    def _init_parser(self):
        usage = 'bin/scramble'
        self.parser = ArgumentParser(usage=usage)
        self.parser.add_argument('-x',
                                 '--example',
                                 default='scramble',
                                 dest='example',
                                 help='Input string to scramble')

    def parse(self, args=None):
        return self.parser.parse_args(args)
