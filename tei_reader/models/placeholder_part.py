#!/usr/bin/env python3
import re

from .placeholder_element import PlaceholderElement

redundant_spaces = re.compile(r'(^ +(?= )|(?<= ) +$)')
class PlaceholderPart(PlaceholderElement):
    """
    Plain-text part without child elements
    """

    is_placeholder = True

    def __init__(self, text):
        super().__init__('part', redundant_spaces.sub('', text))
