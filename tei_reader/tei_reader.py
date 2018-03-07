#!/usr/bin/env python3
import re
from os import path

import lxml.etree as ET
import lxml.objectify as objectify

from bs4 import BeautifulSoup
from .models import Corpora

class TeiReader:
    __xmlns = re.compile(r' *xmlns="[^"]*" *')
    __invalid_ampersand = re.compile(r'&(?=[ <])')
    __xslt = ET.parse(path.join(path.dirname(__file__), "transform", "tei-transform.xsl"))
    __transform = ET.XSLT(__xslt)

    def __do_transform(self, content):
        try:
            dom = ET.fromstring(content)
        except ET.XMLSyntaxError:
            # fallback to Beautiful Soup if there are some oddities in the XML file
            dom = ET.fromstring(bytes(bytearray(str(BeautifulSoup(content, "xml")), encoding='utf-8')))

        return Corpora(self.__transform(dom).getroot())

    def __clean_line(self, line):
        line = self.__xmlns.sub('', line)
        line = self.__invalid_ampersand.sub('&amp;', line)
        return line

    def __clean_lines(self, lines):
        return bytes(bytearray(''.join(self.__clean_line(line) for line in lines), encoding='utf-8'))

    def __clean_file(self, filename):
        with open(filename, encoding='utf-8') as file:
            return self.__clean_lines(file.readlines())

    def read_file(self, file_name):
        content = self.__clean_file(file_name)
        return self.__do_transform(content)

    def read_string(self, content):
        cleaned = self.__clean_lines(content.split('\n'))
        return self.__do_transform(cleaned)
