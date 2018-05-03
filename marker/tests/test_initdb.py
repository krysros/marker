import unittest


class TestInitializeDB(unittest.TestCase):

    def test_usage(self):
        from ..scripts.initializedb import main
        with self.assertRaises(SystemExit):
            main(argv=['foo'])
