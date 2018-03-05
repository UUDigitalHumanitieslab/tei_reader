#!/usr/bin/env python3

class PlaceholderElement:
    def __init__(self, tag, text=None):
        self.tag = tag
        self.parts = []
        if text != None:
            self.text = text

    @property
    def attributes(self):
        return {}

    @property
    def divisions(self):
        """
        Recursively get all the text divisions flattened and in document order. If an element contains parts or text without tag. Those will be returned in order and wrapped with a TextDivision.
        """
        return []
        
    @property
    def xml(self):
        return self.text

    def tostring(self, inject):
        """
        Convert an element to a single string and allow the passed inject method to place content before any
        element.
        """

        return f'{inject(self)}{self.text}'
