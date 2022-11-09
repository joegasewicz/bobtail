[![Python package](https://github.com/joegasewicz/bobtail/actions/workflows/python-package.yml/badge.svg)](https://github.com/joegasewicz/bobtail/actions/workflows/python-package.yml)
[![Upload Python Package](https://github.com/joegasewicz/bobtail/actions/workflows/python-publish.yml/badge.svg)](https://github.com/joegasewicz/bobtail/actions/workflows/python-publish.yml)
[![GitHub license](https://img.shields.io/github/license/joegasewicz/bobtail)](https://github.com/joegasewicz/bobtail/blob/master/LICENSE.md)

[//]: # (![PyPI - Python Version]&#40;https://img.shields.io/pypi/pyversions/bobtail&#41;)

# Bobtail
A little Python http framework


## Install
```
pip install bobtail
```

### Getting Started
```python
from bobtail import BobTail, Request

    class Images:

        def get(self, req: Request):
            return {
                       "users": [{"id: 1"}, {"id: 2"}]
                   }, 200

        def post(self, req: Request):
            return None, 202

        def delete(self, req: Request):
            return None, 201

        def put(self, req: Request):
            return {
                       "id": 1,
                   }, 202

        def patch(self, req: Request):
            return {
                       "id": 1,
                   }, 202

    routes = [
        (Images(), "/images")
    ]

    app = BobTail(routes=routes)

```
