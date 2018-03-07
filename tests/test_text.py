import unittest
from difflib import Differ
from xml.dom import minidom
from os import linesep

from .context import get_files, tei_reader
from pprint import pprint

class TestText(unittest.TestCase):
    def test_files(self):
        differ = Differ()
        reader = tei_reader.TeiReader()

        for (tei, expected) in zip(get_files('tei.xml'), get_files('out.txt')):
            corpora = reader.read_file(tei)
            transformed = corpora.text
            with open(expected, encoding='utf-8') as f:
                diffs = list(diff for diff in differ.compare(
                    [line.strip() for line in f.readlines()],
                    [line.strip() for line in transformed.splitlines(keepends=False)]))
                self.assertEqual(len([diff for diff in diffs if diff[0:2] != '  ']), 0, f"{tei} not transformed as expected:\n{linesep.join(diffs)}")

if __name__ == '__main__':
    unittest.main()
