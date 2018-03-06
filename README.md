[![Build Status](https://travis-ci.org/UUDigitalHumanitieslab/tei_reader.svg?branch=master)](https://travis-ci.org/UUDigitalHumanitieslab/tei_reader)

# Python 3 Library for Reading the Text Content and Metadata of TEI P5 (Lite) Files

The library focuses on extracting the main text content from a file and provide the available metadata about the text.

# TL;DR

```bash
pip install tei-reader
```

```python
from tei_reader import TeiReader
reader = TeiReader()
corpora = reader.read_file('example-tei.xml') # or read_string
print(corpora.text)

# show element attributes before the actual element text
print(corpora.tostring(lambda x, text: str(list(a.key + '=' + a.text for a in x.attributes)) + text))
```

# More Explanation
A reader can be opened using `TeiReader()`. It is then possible to either call `read_file(file_name)` or `read_string(str)`. Both will return a `Corpora` object containing the following properties:

| Property | Description |
| --- | --- |
| `corpora[]` |  A corpora can contain sub-corpora. |
| `documents[]` | The `Document` objects directly part of this corpora. |

`Corpora` and `Document` all inherit from `Element`. In all objects deriving from this it is possible to call:

| Property | Description
| --- | --- |
| `attributes{}` | Contain attributes applicable to this element. If an attribute contains attributes these are also returned. (e.g. `encodingDesc::editorialDecl::normalization`) |
| `text` | Get the entire text content as `str` |
| `divisions[]` | Recursively get all the text divisions in document order. If an element contains parts or text without tag. Those will be returned in order and wrapped with a `PlaceholderDivision`. |
| `parts[]` | Recursively get the parts in document order constituting the entire text e.g. if something has emphasis, a footnote or is marked as foreign. Text without a container element will be returned in order and wrapped with a `PlaceholderPart`. |

`Attribute`, `PlaceholderDivision` and `PlaceholderPart` all support the same properties as `Element`.

# Upload to PyPi

```bash
python setup.py sdist
twine upload dist/*
```
