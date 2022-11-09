import pytest

from wsgi import BobTail
from .mock_environ import mock_environ

def test_bobtail():
    class Images:

        def get(self):
            return f"It Works!"

        def post(self):
            pass

        def delete(self):
            pass

        def put(self):
            pass


    routes = [
        (Images, "/images")
    ]

    app = BobTail(routes=routes)

    def start_response(status, response_headers):
        pass

    res = app(mock_environ, start_response)
    assert res == [b"Hello World!\n"]


