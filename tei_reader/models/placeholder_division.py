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
        return self.tostring(lambda element, text: text)

    @property
    def xml(self):
        return ''.join(part.xml for part in self.parts)

    def tostring(self, inject):
        """
        Convert an element to a single string and allow the passed inject method to place content before any
        element.
        """
        injected_parts = ''
        for part in self.parts:
            injected = part.tostring(inject)
            tei_tag = next(
                (attribute for attribute in part.attributes if attribute.key == "tei-tag"), None)
            if tei_tag and tei_tag.text == "w" and injected_parts:
                # make sure words can be tokenized correctly
                if injected_parts and injected_parts[-1] != ' ':
                    injected_parts += ' '
                injected_parts += injected.strip() + ' '
            else:
                injected_parts += injected

        return inject(self, injected_parts)
