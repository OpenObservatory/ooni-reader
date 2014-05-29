import unittest

from oonireader.data_formats import Entry

class TestDataFormat(unittest.TestCase):
    def test_entry(self):
        entry = {
            'spam': 'eggs',
            'spam2': {'eggs2': 1},
            'spam': 'eggs',
            'spam': 'eggs',
            'spam': 'eggs',
        }
        e = Entry(entry)
        assert e.spam == 'eggs'
