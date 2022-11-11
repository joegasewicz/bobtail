import pytest

from bobtail.wsgi import BobTail
from bobtail.request import Request
from tests.mock_environ import mock_environ
from tests.fixtures import bobtail_app


def test_handlers(bobtail_app):
    class Images:

        def get(self, req, res):
            res.set_body({"users": [{"id": 1}, {"id": 2}]})
            res.set_status(200)

        def post(self, req, res):
            res.set_status(202)

        def delete(self, req, res):
            res.set_body(None)
            res.set_status(201)

        def put(self, req, res):
            res.set_body({"id": 1})
            res.set_status(202)

        def patch(self, req, res):
            res.set_body({"id": 1})
            res.set_status(202)

    routes = [
        (Images(), "/images")
    ]

    app = bobtail_app(routes=routes)

    # GET
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "GET"}
    data = app(environ, lambda s, r: None)
    assert app.response.body == {"users": [{"id": 1}, {"id": 2}]}
    assert app.response.status == 200
    assert data == [b'{\n  "users": [\n    {\n      "id": 1\n    },\n    {\n      "id": 2\n    }\n' b'  ]\n}']

    # POST
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "POST"}
    data = app(environ, lambda s, r: None)
    assert data == []
    assert app.response.body is None
    assert app.response.status == 202

    # # DELETE
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "DELETE"}
    data = app(environ, lambda s, r: None)
    assert data == []
    assert app.response.body is None
    assert app.response.status == 201

    # PUT
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "PUT"}
    data = app(environ, lambda s, r: None)
    assert data == [b'{\n  "id": 1\n}']
    assert app.response.body == {"id": 1}
    assert app.response.status == 202

    # PATCH
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "PATCH"}
    data = app(environ, lambda s, r: None)
    assert data == [b'{\n  "id": 1\n}']
    assert app.response.body == {"id": 1}
    assert app.response.status == 202

    # Check no middleware is added
    assert len(app.middleware.middlewares) == 0


def test_headers():
    class Images:

        def get(self, req, res):
            res.set_headers({"Content-type": "text/plain"})
            res.set_status(200)
            res.set_body({})

    routes = [
        (Images(), "/images")
    ]

    app = BobTail(routes=routes)

    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "GET"}
    _ = app(environ, lambda s, r: None)
    assert app.response.headers["Content-type"] == "text/plain"
