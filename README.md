[![Python package](https://github.com/joegasewicz/bobtail/actions/workflows/python-package.yml/badge.svg)](https://github.com/joegasewicz/bobtail/actions/workflows/python-package.yml)
[![Upload Python Package](https://github.com/joegasewicz/bobtail/actions/workflows/python-publish.yml/badge.svg)](https://github.com/joegasewicz/bobtail/actions/workflows/python-publish.yml)
[![GitHub license](https://img.shields.io/github/license/joegasewicz/bobtail)](https://github.com/joegasewicz/bobtail/blob/master/LICENSE.md)

[//]: # (![PyPI - Python Version]&#40;https://img.shields.io/pypi/pyversions/bobtail&#41;)

![Bobtail](bobtail.png?raw=true "Bobtail")
A little Python http framework


## Install
```
pip install bobtail
```

### Getting Started
An example of the smallest Bobtail app
```python
from typing import Tuple, Optional, Dict
from bobtail import AbstractRoute, Request, Response
def test_headers():
    class Images:

        def get(self, req, res):
            res.set_status(200)
            res.set_body({id: 1})

    routes = [
        (Images(), "/images")
    ]

    app = BobTail(routes=routes)

```
