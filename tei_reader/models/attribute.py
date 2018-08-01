#!/usr/bin/env python3
from .element import Element
from .placeholder_attribute import PlaceholderAttribute
from .util import to_key

class Attribute(Element):
    def __init__(self, node, parent_keys):
        super().__init__(node)
        self.parent_keys = parent_keys

    @property
    def attributes(self):
        if 'id' in self.node.attrib:
            yield PlaceholderAttribute('id', self.node.attrib['id'], self.__path)

        if 'tei-tag' in self.node.attrib:
            yield PlaceholderAttribute('tei-tag', self.node.attrib['tei-tag'], self.__path)

        """Contain attributes applicable to this element"""
        for attributes in self.node.iterchildren('attributes'):
            for attribute in self.__iter_attributes__(attributes, self.__path):
                yield attribute

    @property
    def key(self):
        return to_key(self.parent_keys, self.__own_key)

    @property
    def __own_key(self):
        try:
            return self.node.attrib["key"]
        except KeyError:
            return ""

    @property
    def __path(self):
        return [key for key in [parent_key for parent_key in self.parent_keys] + [self.__own_key] if key]
