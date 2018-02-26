#!/usr/bin/env python3
from .element import Element

class Division(Element):
    @property
    def text(self):
        """Get the entire text content as str"""
        divisions = list(self.divisions)
        if len(divisions) == 0:
            return ''
        elif len(divisions) == 1:
            return divisions[0].text.strip()
        else:
            return super().text
