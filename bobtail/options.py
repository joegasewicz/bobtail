from abc import ABC


class BaseOptions(ABC):
    """
    To define port, static directory, template directory etc. you can
    create a concrete version of the BaseOptions abstract class.
    For Example::

        from bobtail.options import BaseOptions

        class Options(BaseOptions):
            PORT = 8001

        app = Bobtail(Options)

    """
    #: The port by default is set to `8000`
    PORT = 8000

    #: The static directory relative path is set by default to `static`
    STATIC_DIR = "static"

    #: The template directory relative path is set by default to `templates`
    TEMPLATE_DIR = "templates"
