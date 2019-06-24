import unittest
from difflib import Differ
from xml.dom import minidom
from os import linesep

from .context import get_files, tei_reader
from pprint import pprint

class TestTransform(unittest.TestCase):
    def test_files(self):
        reader = tei_reader.TeiReader()
        tei_files = get_files('tei.xml')
        expected_files = get_files('out.xml')
        self.assertEqual(len(tei_files), len(expected_files))
        for (tei, expected) in zip(tei_files, expected_files):
            corpora = reader.read_file(tei)
            self.check_corpora(corpora, expected, '{0} (as file)'.format(tei))
            with open(tei, encoding='utf-8') as f:
                corpora = reader.read_string(f.read())
                self.check_corpora(corpora, expected, '{0} (as string)'.format(tei))


    def check_corpora(self, corpora, expected, id):
        differ = Differ()
        transformed = minidom.parseString(corpora.xml).toprettyxml(indent="    ").replace("&quot;", '"')
        with open(expected, encoding='utf-8') as f:
            diffs = list(diff for diff in differ.compare(
                [line.strip() for line in f.readlines()],
                [line.strip() for line in transformed.splitlines(keepends=False) if line.strip() != '']))
            self.assertEqual(len([diff for diff in diffs if diff[0:2] != '  ']), 0, "{0} not transformed as expected:\n{1}".format(id, linesep.join(diffs)))

if __name__ == '__main__':
    unittest.main()
