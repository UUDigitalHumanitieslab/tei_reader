import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from os import linesep, listdir, path
from os.path import isfile, join

import tei_reader

test_dir = path.join(path.dirname(__file__), 'xslt')

def get_files(pattern):
    return sorted([path.join(test_dir, f) for f in listdir(test_dir) if f.find(pattern) >= 0])
