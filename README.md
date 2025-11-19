[![Python package](https://github.com/joegasewicz/bobtail/actions/workflows/python-package.yml/badge.svg)](https://github.com/joegasewicz/bobtail/actions/workflows/python-package.yml)
[![GitHub license](https://img.shields.io/github/license/joegasewicz/bobtail)](https://github.com/joegasewicz/bobtail/blob/master/LICENSE.md)

[//]: # (![PyPI - Python Version]&#40;https://img.shields.io/pypi/pyversions/bobtail&#41;)

![Bobtail](bobtail.png?raw=true "Bobtail")
A little Python http framework

⚠️ *Ready to use in `v0.1.0`, production ready in `v1.0.0`*

Read the [docs](https://bobtail.readthedocs.io/en/latest/)

## Install
```
pipenv install bobtail
```

### Getting Started
An example of the smallest Bobtail app
```python
from bobtail import BobTail, AbstractRoute, Request, Response

class Blogs:

    def get(self, req, res):
        res.set_body({id: 1})

routes = [
    (Blogs(), ["/blogs", "blogs/{blog_id:int}"])
]

if __name__ == "__main__":
    bobtail = BobTail(routes=routes)
    bobtail.run(port=8000)
```

### Routes
Declare routes with a list of tuples, where the first item uis the route handler class & second item
is a list of paths to match against.

```python
routes = [
    (Videos(), ["/videos"]),
    (Files(), ["/files/new/{true:bool}"]),
    (Product(), [
        "/products/{product_id:int}/details",
        "/products/{product_id:int}",
        "/products",
        "/products/{product_id:int}/details/{detail_is:int}",
    ]),
    (Images(), ["/static/*"]),
]
```

### Options
To define port, static directory, template directory etc. you can
create a concrete version of the BaseOptions abstract class. See the [docs](https://bobtail.readthedocs.io/en/latest/options.html) for more info.
```python
from bobtail.options import BaseOptions

class Options(BaseOptions):
    PORT = 8001

app = Bobtail(Options)
```
### Middleware
Bobtail middleware

#### Using third party middleware
```python
from bobtail_logger import BobtailLogger

app = Bobtail(routes=routes)

# Here we are using `bobtail-logger.py` logging middleware
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
### Query Params
This method returns a dict og query params where the key
is on the left side of the `=` sign & the value is pn the right.
For example:
```python
# for route "/images?name=joe&age=48"
def get(self, req: Request, res: Response):
    result = req.get_params() # {"name": "joe", "age": "48"}
```

### Static Files
To declare a static route postfix a `*` to the route's path::
```python
from bobtail import BobTail AbstractRoute, BaseOptions
from bobtail_jinja2 import BobtailJinja2

routes = [
    (Static(), "/static/*"),
]

class Options(BaseOptions):
    STATIC_DIR = "app/static"
    TEMPLATE_DIR = "app/templates"

blog = BobTail(routes=routes, options=Options())
blog.use(BobtailJinja2(template_dir="app/templates"))
```
Calling `set_static` from within a route method will render a static
file such as a .css, .js or a media type file. The :class:`~BaseOptions`
class sets the `STATIC_DIR` directory.
```python

    class Static(AbstractRoute):
        def get(self, req: Request, res: Response) -> None:
            res.set_static(req.path)
```
You can set the static file path using the :class:`~BaseOptions`.
```python

class Options(BaseOptions):
    STATIC_DIR = "/static"

# Now in a route handler we can access static directory the via options
class Static(AbstractRoute):
    def get(self, req: Request, res: Response) -> None:
        res.set_static(req.path)
```
By default, `STATIC_DIR` is set to `/static`, if your static file is nested
within a Python package, for example `app/static` the set as `STATIC_DIR = "app/static"`

To render an image from within a Jinja2 template include the full path including the
static directory name or path. For example::
```html
<!-- if STATIC_DIR = "/static" -->
<body>
    <img src="/static/imgs/cat1.jpg" />
</body>
```
OR without the first forward slash::
```html
<body>
    <img src="static/imgs/cat1.jpg" />
</body>
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
    def get(self, req: Request, res: Response) -> None:
        pass
    
    def post(self, req: Request, res: Response) -> None:
        pass

    def put(self, req: Request, res: Response) -> None:
        pass

    def delete(self, req: Request, res: Response) -> None:
        pass

```

### Run Bobtail in Production
Install a WSGI compatible server such as [Gunicorn](https://gunicorn.org/)
```bash
# This is an example setup, `api` refers to file & `app` refers to a Bobtail instance.
 pip install gunicorn
 gunicorn api:app 
```
