#!/usr/bin/env python3
from .placeholder_element import PlaceholderElement

class PlaceholderAttribute(PlaceholderElement):
    """
    Division to group loose parts (which aren't direct children of a division)
    """
        
    def __init__(self, key, text):
        super().__init__('attribute', text)
        self.key = key
