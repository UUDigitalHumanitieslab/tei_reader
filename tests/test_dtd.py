#!/usr/bin/env python3
import unittest
from os import path
import lxml.etree as ET

from .context import get_files

class TestAttributes(unittest.TestCase):
    def test_dtd(self):
        """
        Check that the test output matches the DTD.
        """

        with open(path.join(path.dirname(__file__), '..', 'transform', 'tei-content.dtd')) as f:
            dtd = ET.DTD(f)
            
        for transformed in (ET.parse(xml) for xml in get_files('out.xml')):
            if not dtd.validate(transformed):
                self.fail(dtd.error_log)