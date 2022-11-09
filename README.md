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
from typing import Tuple, Optional, Dict

from bobtail import AbstractRoute, Request, Response


class Images(AbstractRoute):
    def get(self, req: Request, res: Response) -> Tuple[Optional[Dict], int]:
        # Use the response object to set the response headers if required (these are the default headers)
        res.headers = [("Content-type", "application/json")]
        return {
            "image": {
                "id": 1,
                "url": "http://localhost:7004",
                "file_name": "sunny.png"
            }
        }, 200

    def post(self, req: Request, res: Response) -> Tuple[Optional[Dict], int]:
        pass

    def put(self, req: Request, res: Response) -> Tuple[Optional[Dict], int]:
        pass

    def delete(self, req: Request, res: Response) -> Tuple[Optional[Dict], int]:
        pass

    routes = [
        (Images(), "/images")
    ]

    app = BobTail(routes=routes)

```
