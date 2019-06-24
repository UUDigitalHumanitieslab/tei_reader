import unittest
from difflib import Differ
from xml.dom import minidom
from os import linesep, path
import sys
sys.path.append(path.dirname(__file__))

from context import get_files, tei_reader
from pprint import pprint

class TestAttributes(unittest.TestCase):
    def test_files(self):
        differ = Differ()
        reader = tei_reader.TeiReader()
        for (tei, expected) in zip(get_files('tei.xml'), get_files('out-attrs.txt')):
            corpora = reader.read_file(tei)
            transformed = corpora.tostring(inject_attributes)
            with open(expected, encoding='utf-8') as f:
                diffs = list(diff for diff in differ.compare(
                    [line.strip() for line in f.readlines()],
                    [line.strip() for line in transformed.splitlines(keepends=False)]))
                self.assertEqual(len([diff for diff in diffs if diff[0:2] != '  ']), 0, "{0} not transformed as expected:\n{1}".format(tei, linesep.join(diffs)))
    
def inject_attributes(element, text):
    attributes = list(element.attributes)
    if not attributes:
        return text

    pairs = '\n'.join('{0}="{1}"'.format(attribute.key, attribute.text.strip()) for attribute in attributes)

    return '[{0}]{1}'.format(pairs, text)

if __name__ == '__main__':
    unittest.main()
