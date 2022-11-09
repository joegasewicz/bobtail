from bobtail.wsgi import BobTail
from bobtail.request import Request
from .mock_environ import mock_environ


def test_bobtail():
    class Images:

        def get(self, req: Request):
            return {
                       "users": [{"id: 1"}, {"id: 2"}]
                   }, 200

        def post(self, req: Request):
            return None, 202

        def delete(self, req: Request):
            return None, 201

        def put(self, req: Request):
            return {
                       "id": 1,
                   }, 202

        def patch(self, req: Request):
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
    assert data == [b"{'users': [{'id: 1'}, {'id: 2'}]}"]
    assert app.response.status == 200

    # POST
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "POST"}
    data = app(environ, lambda s, r: None)
    assert data is None
    assert app.response.status == 202

    # DELETE
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "DELETE"}
    data = app(environ, lambda s, r: None)
    assert data is None
    assert app.response.status == 201

    # PUT
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "PUT"}
    data = app(environ, lambda s, r: None)
    assert data == [b"{'id': 1}"]
    assert app.response.status == 202

    # PATCH
    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "PATCH"}
    data = app(environ, lambda s, r: None)
    assert data == [b"{'id': 1}"]
    assert app.response.status == 202
