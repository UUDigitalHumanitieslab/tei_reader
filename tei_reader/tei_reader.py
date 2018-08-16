#!/usr/bin/env python3
import re
from os import path

import lxml.etree as ET
import lxml.objectify as objectify

from bs4 import BeautifulSoup
from .models import Corpora

class TeiReader:
    __xmlns = re.compile(r' *xmlns(|\:\w+)="[^"]*"')
    __invalid_ampersand = re.compile(r'&(?=[ <])')
    __xslt = ET.parse(path.join(path.dirname(__file__), "transform", "tei-transform.xsl"))
    __transform = ET.XSLT(__xslt)

    def __do_transform(self, content):
        try:
            dom = ET.fromstring(content)
        except ET.XMLSyntaxError:
            # fallback to Beautiful Soup if there are some oddities in the XML file
            dom = ET.fromstring(bytes(bytearray(str(BeautifulSoup(content, "xml")), encoding='utf-8')))

        xml = self.__assign_beginnings(self.__transform(dom).getroot())
        return Corpora(xml)

    def __assign_beginnings(self, xml: ET.Element) -> ET.Element:
        def rename_n_attribute(element, name):
            for n in element.xpath('attributes/attribute[@key]'):
                n.attrib['key'] = name
        
        # A div can contain parts, but parts cannot contain divs.
        # It is import to respect this difference, because the
        # corpus2alpinoreader assumes that a sentence/utterance can be
        # splitted over parts, but not over divs.
        for line in xml.xpath('//lb'):
            rename_n_attribute(line, 'line')
            division = False
            for sibling in line.itersiblings():
                if sibling.tag in ['lb', 'pb']:
                    break
                for descendant in sibling.iterdescendants():
                    if descendant.tag in ['lb', 'pb']:
                        break
                    if descendant.tag == 'div':
                        division = True
                line.append(sibling)
            line.tag = 'div' if division else 'part'

        for page in xml.xpath('//pb'):
            rename_n_attribute(page, 'page')
            division = False
            for sibling in page.itersiblings():
                if sibling.tag == 'pb':
                    break
                for descendant in sibling.iterdescendants():
                    if descendant.tag == 'pb':
                        break
                    if descendant.tag == 'div':
                        division = True
                page.append(sibling)
            page.tag = 'div' if division else 'part'

        return xml

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
