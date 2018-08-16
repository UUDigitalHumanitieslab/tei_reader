#!/usr/bin/env python3
"""
Script for updating the output files using the current behavior.
"""
import sys
sys.path.append("..") 
sys.path.append(".") 

from xml.dom import minidom
from os import linesep, path, listdir

from tei_reader import TeiReader
from pprint import pprint

from test_attributes import inject_attributes

test_dir = path.join(path.dirname(__file__), 'xslt')
def get_files(pattern):
    return [path.join(test_dir, f) for f in listdir(test_dir) if f.find(pattern) >= 0]

def write_transform(corpora, output):
    transformed = minidom.parseString(corpora.xml).toprettyxml(indent="    ").replace("&quot;", '"')
    with open(output, mode='w', encoding='utf-8') as f:
        f.writelines(line + '\n' for line in transformed.splitlines()
            if line.strip() != '')

def write_text(corpora, output):
    transformed = corpora.text
    with open(output, mode='w', encoding='utf-8') as f:
        f.write(transformed)

def write_attributes(corpora, output):
    transformed = corpora.tostring(inject_attributes)
    with open(output, mode='w', encoding='utf-8') as f:
        f.write(transformed)

reader = TeiReader()
tei_files = get_files('tei.xml')

for tei in tei_files:
    corpora = reader.read_file(tei)
    write_transform(corpora, tei.replace('tei.xml', 'out.xml'))
    write_text(corpora, tei.replace('tei.xml', 'out.txt'))
    write_attributes(corpora, tei.replace('tei.xml', 'out-attrs.txt'))
