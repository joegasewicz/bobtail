from abc import ABC


class BaseOptions(ABC):
    PORT = 8000
    STATIC_DIR = "static"
    TEMPLATE_DIR = "templates"
