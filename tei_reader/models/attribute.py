#!/usr/bin/env python3
from .element import Element

class Attribute(Element):
    def __init__(self, node, parent_keys):
        super().__init__(node)
        self.parent_keys = parent_keys

    @property
    def key(self):
        return "::".join(key for key in [parent_key for parent_key in self.parent_keys] + [self.__own_key] if key)

    @property
    def __own_key(self):
        try:
            return self.node.attrib["key"]
        except KeyError:
            return ""

