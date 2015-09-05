import unittest

from lib import Options

class TestCommandLineParameters(unittest.TestCase):

    def setUp(self):
        self.options = Options()

    def test_defaults_options_are_set(self):
        opts = self.options.parse()
        self.assertEquals(opts.example, 'scramble')

    def test_options_example_is_set(self):
        opts = self.options.parse(['-x', 'foobar'])
        self.assertEquals(opts.example, 'foobar')

        opts = self.options.parse(['--example', 'xyz'])
        self.assertEquals(opts.example, 'xyz')


if __name__ == '__main__':
    unittest.main()
