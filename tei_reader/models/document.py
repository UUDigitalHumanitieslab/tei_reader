#!/usr/bin/env python3
from .element import Element

class Document(Element):
    def __init__(self, node, corpus):
        super().__init__(node)
        self.corpus = corpus
