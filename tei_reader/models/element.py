#!/usr/bin/env python3
import lxml.etree as ET
from .placeholder_attribute import PlaceholderAttribute

class Element:
    def __init__(self, node):
        self.node = node

    @property
    def tag(self):
        return self.node.tag

    @property
    def attributes(self):
        if 'id' in self.node.attrib:
            yield PlaceholderAttribute('id', self.node.attrib['id'])

        if 'tei-tag' in self.node.attrib:
            yield PlaceholderAttribute('tei-tag', self.node.attrib['tei-tag'])

        """Contain attributes applicable to this element"""
        for attributes in self.node.iterchildren('attributes'):
            for attribute in self.__iter_attributes__(attributes):
                yield attribute

    @property
    def text(self):
        """Get the entire text content as str"""
        return self.tostring(lambda element, text: text)

    @property
    def divisions(self):
        """
        Recursively get all the text divisions directly part of this element. If an element contains parts or text without tag. Those will be returned in order and wrapped with a TextDivision.
        """

        from .placeholder_division import PlaceholderDivision
        
        placeholder = None
        for item in self.__parts_and_divisions:
            if item.tag == 'part':
                if not placeholder:
                    placeholder = PlaceholderDivision()
                placeholder.parts.append(item)
            else:
                if placeholder:
                    yield placeholder
                    placeholder = None
                yield item
        if placeholder:
            yield placeholder

    @property
    def parts(self):
        """
        Recursively get the parts flattened and in document order constituting the entire text e.g. if something has emphasis, a footnote or is marked as foreign. Text without a container element will be returned in order and wrapped with a TextPart.
        """

        for item in self.__parts_and_divisions:
            if item.tag == 'part' and item.is_placeholder:
                yield item
            else:
                for part in item.parts:
                    yield part

    @property
    def xml(self):
        return ET.tostring(self.node, encoding='unicode')

    @property
    def __parts_and_divisions(self):
        """
        The parts and divisions directly part of this element.
        """

        from .division import Division
        from .part import Part
        from .placeholder_part import PlaceholderPart

        text = self.node.text
        if text:
            stripped_text = text.replace('\n', '')
            if stripped_text.strip():
                yield PlaceholderPart(stripped_text)

        for item in self.node:
            if item.tag == 'part':
                yield Part(item)
            elif item.tag == 'div':
                yield Division(item)
            
            if item.tail:
                stripped_tail = item.tail.replace('\n', '')
                if stripped_tail.strip():
                    yield PlaceholderPart(stripped_tail)

    def __iter_attributes__(self, attributes, parents = []):
        # do the import here, because Attribute dependens on Element
        from .attribute import Attribute
        if 'key' in attributes.attrib:
            parents = parents + [attributes.attrib['key']]

        for attribute in attributes.iterchildren('attribute'):
            yield Attribute(attribute, parents)
            for sub_attributes in attribute.iter('attributes'):
                if 'key' in attribute.attrib:
                    sub_parents = parents + [attribute.attrib['key']]
                else:
                    sub_parents = parents
                for sub_attribute in self.__iter_attributes__(sub_attributes, sub_parents):
                    yield sub_attribute


    def tostring(self, inject):
        """
        Convert an element to a single string and allow the passed inject method to place content before any
        element.
        """

        return inject(self, '\n'.join(f'{division.tostring(inject)}' for division in self.divisions))
