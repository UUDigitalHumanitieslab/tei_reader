#!/usr/bin/env python3
from .document import Document
from .element import Element

class Corpora(Element):
    @property
    def corpora(self):
        for corpora in self.node.iterchildren('corpora'):
            yield Corpora(corpora)

    @property
    def documents(self):
        for item in self.node:
            if item.tag == 'document':
                yield Document(item, self)
            elif item.tag == 'corpora':
                for document in Corpora(item).documents:
                    yield document

    def tostring(self, inject):
        """Get the entire text content as str"""
        return inject(self, '\n'.join(document.tostring(inject) for document in self.documents))
