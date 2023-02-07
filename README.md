[![Python package](https://github.com/joegasewicz/bobtail/actions/workflows/python-package.yml/badge.svg)](https://github.com/joegasewicz/bobtail/actions/workflows/python-package.yml)
[![Upload Python Package](https://github.com/joegasewicz/bobtail/actions/workflows/python-publish.yml/badge.svg)](https://github.com/joegasewicz/bobtail/actions/workflows/python-publish.yml)
[![GitHub license](https://img.shields.io/github/license/joegasewicz/bobtail)](https://github.com/joegasewicz/bobtail/blob/master/LICENSE.md)

[//]: # (![PyPI - Python Version]&#40;https://img.shields.io/pypi/pyversions/bobtail&#41;)

![Bobtail](bobtail.png?raw=true "Bobtail")
A little Python http framework

⚠️ *Ready to use in `v0.1.0`, production ready in `v1.0.0`*

Read the [docs](https://bobtail.readthedocs.io/en/latest/)

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

### Middleware
Bobtail middleware

#### Using third party middleware
```python
from bobttail_logger import BobtailLogger

app = Bobtail(routes=routes)

# Here we are using `bobtail-logger` logging middleware
app.use(BobtailLogger())
```

Middleware currently available
- [bobtail-cors](https://github.com/joegasewicz/bobtail-cors)
- [bobtail-logger](https://github.com/joegasewicz/bobtail-logger)
- [bobtail-upload](https://github.com/joegasewicz/bobtail-upload)
- [bobtail-jinja2](https://github.com/joegasewicz/bobtail-jinja2)


Creating custom middleware example. A Middleware object must implement `AbstractMiddleware`. 

```python
from bobtail import Request, Response
from bobtail.middleware import AbstractMiddleware, Tail

class BobtailCors(AbstractMiddleware):

    def run(self, req: Request, res: Response, tail: Tail) -> None:
        res.set_headers({
            "Access-Control-Allow-Origin": "*",
        })
        tail(req, res)
```

### HTML Templates
Bobtail does not ship with a templating engine directly, but you can install and use
a templating engine with ease via middleware.

Currently, there is middleware support for Jinja2, for example
```python
from bobtail_jinja2 import BobtailJinja2

blog = BobTail(routes=routes)
blog.use(BobtailJinja2(template_dir="templates"))
```
Then to use in a request handler
```python
def get(self, req: Request, res: Response) -> None:
    res.jinja2.render(res, "layout.jinja2", data={"name": "joe"})
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
## Request

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

### Request Body
- JSON
 ```python
# marshals json to a python dict
req.get_json()
```
- Plain Text
 ```python
# returns a string
req.get_body()
```
- Urlencoded form data
 ```python
# returns a pyton dict
req.get_form_data()
```
- Multipart form data
 ```python
# returns a pyton dict
req.get_multipart_data()
```

The `Request` object provides methods to easily get form values. By default, if a form value
doesn't exist, then either `FormDataError` or `MultipartFormDataError` exceptions will be raised.

- Get Form Field Value
```python
from bobtail.exceptions import FormDataError
try:
    email = req.form.get_field("email")
except FormDataError:
    pass # handle no form value
```

- Get Multipart Form Field Value
```python
from bobtail.exceptions import MultipartFormDataError
try:
    email = req.multipart.get_field("email")
except MultipartFormDataError:
    pass # handle no multipart form value
```

- Get Multipart Form File Value
```python
from bobtail.exceptions import MultipartFormDataError
try:
    email = req.multipart.get_file("image")
except MultipartFormDataError:
    pass # handle no multipart form value
```

- Get Multipart Form File Name
```python
from bobtail.exceptions import MultipartFormDataError
try:
    email = req.multipart.get_name("image")
except MultipartFormDataError:
    pass # handle no multipart form value
```

- Get Multipart Form File Data
```python
from bobtail.exceptions import MultipartFormDataError
try:
    email = req.multipart.get_data("image")
except MultipartFormDataError:
    pass # handle no multipart form value
```

- Get Multipart Form File Mimetype
```python
from bobtail.exceptions import MultipartFormDataError
try:
    email = req.multipart.get_mimetype("image")
except MultipartFormDataError:
    pass # handle no multipart form value
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

