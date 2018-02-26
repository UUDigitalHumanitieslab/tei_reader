import unittest
from difflib import Differ
from xml.dom import minidom
from os import linesep

from .context import get_files, tei_reader
from pprint import pprint

class TestTransform(unittest.TestCase):
    def test_files(self):
        reader = tei_reader.TeiReader()

        for (tei, expected) in zip(get_files('tei.xml'), get_files('out.xml')):
            corpora = reader.read_file(tei)
            self.check_corpora(corpora, expected, f'{tei} (as file)')            
            with open(tei) as f:
                corpora = reader.read_string(f.read())
                self.check_corpora(corpora, expected, f'{tei} (as string)')


    def check_corpora(self, corpora, expected, id):
        differ = Differ()
        transformed = minidom.parseString(corpora.xml).toprettyxml(indent="    ").replace("&quot;", '"')
        with open(expected) as f:
            diffs = list(diff for diff in differ.compare(
                [line.strip() for line in f.readlines()],
                [line.strip() for line in transformed.splitlines(keepends=False) if line.strip() != '']))
            self.assertEqual(len([diff for diff in diffs if diff[0:2] != '  ']), 0, f"{id} not transformed as expected:\n{linesep.join(diffs)}")

if __name__ == '__main__':
    unittest.main()
