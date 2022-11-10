[![Python package](https://github.com/joegasewicz/bobtail/actions/workflows/python-package.yml/badge.svg)](https://github.com/joegasewicz/bobtail/actions/workflows/python-package.yml)
[![Upload Python Package](https://github.com/joegasewicz/bobtail/actions/workflows/python-publish.yml/badge.svg)](https://github.com/joegasewicz/bobtail/actions/workflows/python-publish.yml)
[![GitHub license](https://img.shields.io/github/license/joegasewicz/bobtail)](https://github.com/joegasewicz/bobtail/blob/master/LICENSE.md)

[//]: # (![PyPI - Python Version]&#40;https://img.shields.io/pypi/pyversions/bobtail&#41;)

![Bobtail](bobtail.png?raw=true "Bobtail")
A little Python http framework


## Install
```
pipenv install bobtail
pipenv install gunicorn
```

### Getting Started
An example of the smallest Bobtail app
```python
from typing import Tuple, Optional, Dict
from bobtail import BobTail, AbstractRoute, Request, Response

class Images:

    def get(self, req, res):
        res.set_body({id: 1})

routes = [
    (Images(), "/images")
]

app = BobTail(routes=routes)

```

### Run
```
pipenv run  gunicorn api:app
```
### Set the Headers
You can set the headers with the `Response` object's `set_headers` method. The default headers
are `Content-Type: application/json`.
```python
class Images:

    def get(self, req, res):
        res.set_headers({"Content-type": "text/plain"})

```

### Set the response status
You can set the status with the `Response` object's `set_status` method. The default status
is always set to `200` if there are no errors.
```python
class Images:

    def get(self, req, res):
        res.set_status(202)

```

### Request Args
You can specify the type of `Request` arguments using curly braces & within the name & type seperated 
by a colon, for example:
```
/images/{id:int}/{name:str}/{is_raining:bool}
```
To access request arguments inside a route handler, use the `Request` object's `get_arg` method, for example:
```python
def get(self, req, res):
    id = req.get_args("id") # int
    name = req.get_args("name") # str
    is_raining = req.get_args("is_raining") # bool
```

### OOP Approach
If you prefer to organise your routes in a more OOP approach, you can implement the
`AbstractRoute` abstract class. It's especially useful when using an IDE like Pycharm
where the IDE will generate automatically all the require methods.
```python
from bobtail import AbstractRoute, Request, Response

# (Pycharm) - right click over the `Image` class name & select `Show context actions`
# then click `implement abstract methods`, then select all and click ok.
class Images(AbstractRoute): 
    pass
```
Which will generate the following:

```python
from bobtail import AbstractRoute, Request, Response


class Images(AbstractRoute):
    def get(self, req: Request, res: Response):
        pass
    
    def post(self, req: Request, res: Response):
        pass

    def put(self, req: Request, res: Response):
        pass

    def delete(self, req: Request, res: Response):
        pass

```