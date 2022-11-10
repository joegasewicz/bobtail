from bobtail.wsgi import BobTail
from bobtail.request import Request
from .mock_environ import mock_environ


def test_handlers():
    class Images:

        def get(self, req, res):
            return {
                       "users": [{"id": 1}, {"id": 2}],
                   }, 200

        def post(self, req, res):
            return None, 202

        def delete(self, req, res):
            return None, 201

        def put(self, req, res):
            return {
                       "id": 1,
                   }, 202

        def patch(self, req, res):
            return {
                       "id": 1,
                   }, 202

    routes = [
        (Images(), "/images")
    ]

    app = BobTail(routes=routes)

    # GET
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "GET"}
    data = app(environ, lambda s, r: None)
    assert data == [b'{\n  "users": [\n    {\n      "id": 1\n    },\n    {\n      "id": 2\n    }\n' b'  ]\n}']
    assert app.response.status == 200

    # POST
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "POST"}
    data = app(environ, lambda s, r: None)
    assert data == []
    assert app.response.status == 202

    # DELETE
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "DELETE"}
    data = app(environ, lambda s, r: None)
    assert data == []
    assert app.response.status == 201

    # PUT
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "PUT"}
    data = app(environ, lambda s, r: None)
    assert data == [b'{\n  "id": 1\n}']
    assert app.response.status == 202

    # PATCH
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "PATCH"}
    data = app(environ, lambda s, r: None)
    assert data == [b'{\n  "id": 1\n}']
    assert app.response.status == 202


def test_headers():
    class Images:

        def get(self, req, res):
            res.headers = {"Content-type", "text/plain"}
            return "Text response!"

    routes = [
        (Images(), "/images")
    ]

    app = BobTail(routes=routes)

    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "GET"}
    _ = app(environ, lambda s, r: None)
    assert app.response.headers == {"Content-type", "text/plain"}
