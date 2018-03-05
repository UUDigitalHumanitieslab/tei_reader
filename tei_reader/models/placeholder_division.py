#!/usr/bin/env python3
from .placeholder_element import PlaceholderElement

class PlaceholderDivision(PlaceholderElement):
    """
    Division to group loose parts (which aren't direct children of a division)
    """
        
    def __init__(self):
        super().__init__('div')

    @property
    def text(self):
        """Get the entire text content as str"""
        return ''.join(part.text for part in self.parts)
        
    @property
    def xml(self):
        return ''.join(part.xml for part in self.parts)
