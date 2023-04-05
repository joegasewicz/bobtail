Static Files
============

To declare a static route postfix a `*` to the route's path

.. code-block:: python

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


Calling `set_static` from within a route method will render a static
file such as a .css, .js or a media type file. The :class:`~BaseOptions`
class sets the `STATIC_DIR` directory.
For example

.. code-block:: python

    class Static(AbstractRoute):
        def get(self, req: Request, res: Response) -> None:
            res.set_static("/static/imgs/cat1.jpg")

You can set the static file path using the :class:`~BaseOptions`.
For example

.. code-block:: python

    class Options(BaseOptions):
        STATIC_DIR = "/static"

    # Now in a route handler we can access static directory the via options

    class Static(AbstractRoute):
        def get(self, req: Request, res: Response) -> None:
            res.set_static(f"{res.options.STATIC_DIR}/imgs/cat1.jpg")

By default, `STATIC_DIR` is set to `/static`, if your static file is nested
within a Python package, for example `app/static` the set as `STATIC_DIR = "app/static"`

To render an image from within a Jinja2 template include the full path including the
static directory name or path. For example

.. code-block:: html

    <!-- if STATIC_DIR = "/static" -->
    <body>
        <img src="/static/imgs/cat1.jpg" />
    </body>

OR without the first forward slash

.. code-block:: html

    <body>
        <img src="static/imgs/cat1.jpg" />
    </body>
