#!/usr/bin/env python3
from .placeholder_element import PlaceholderElement
from .util import to_key

class PlaceholderAttribute(PlaceholderElement):
    """
    Division to group loose parts (which aren't direct children of a division)
    """
        
    def __init__(self, key, text, parent_keys = []):
        super().__init__('attribute', text)
        self.__own_key = key
        self.parent_keys = parent_keys

    @property
    def key(self):
        return to_key(self.parent_keys, self.__own_key)
