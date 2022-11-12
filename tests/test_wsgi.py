from tests.fixtures import bobtail_app
from tests.fixtures import (
    route_class_one,
    route_class_two,
    middle_cors,
    middle_logger,
)

from bobtail.wsgi import BobTail


class TestBobtail:

    app: BobTail = None

    def teardown_method(self, bobtail_app):
        self.app = None

    def test_use(self, bobtail_app, middle_cors, middle_logger):

        class Images:

            def get(self, req, res):
                res.set_headers({"Content-type": "text/plain"})
                res.set_status(200)
                res.set_body({})

        routes = [
            (Images(), "/images")
        ]

        self.app = bobtail_app(routes=routes)

        # Check no middleware is added
        assert self.app.middleware.middlewares is None

        self.app.use(middle_cors)
        self.app.use(middle_logger)

        assert len(self.app.middleware.middlewares) == 2

        environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "GET"}
        _ = self.app(environ, lambda s, r: None)
        assert self.app.response.headers["Access-Control-Allow-Origin"] == "*"

    def test_handlers(self, bobtail_app, route_class_one):

        routes = [
            (route_class_one, "/images")
        ]
        self.app = bobtail_app(routes=routes)

        # GET
        environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "GET"}
        data = self.app(environ, lambda s, r: None)
        assert self.app.response.body == {"users": [{"id": 1}, {"id": 2}]}
        assert self.app.response.status == 200
        assert data == [b'{\n  "users": [\n    {\n      "id": 1\n    },\n    {\n      "id": 2\n    }\n' b'  ]\n}']

        # POST
        environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "POST"}
        data = self.app(environ, lambda s, r: None)
        assert data == []
        assert self.app.response.body is None
        assert self.app.response.status == 202

        # # DELETE
        environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "DELETE"}
        data = self.app(environ, lambda s, r: None)
        assert data == []
        assert self.app.response.body is None
        assert self.app.response.status == 201

        # PUT
        environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "PUT"}
        data = self.app(environ, lambda s, r: None)
        assert data == [b'{\n  "id": 1\n}']
        assert self.app.response.body == {"id": 1}
        assert self.app.response.status == 202

        # PATCH
        environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "PATCH"}
        data = self.app(environ, lambda s, r: None)
        assert data == [b'{\n  "id": 1\n}']
        assert self.app.response.body == {"id": 1}
        assert self.app.response.status == 202

        # Check no middleware is added
        assert self.app.middleware.middlewares is None

    def test_headers(self, bobtail_app, route_class_two):

        routes = [
            (route_class_two, "/images")
        ]

        self.app = bobtail_app(routes=routes)

        # Check no middleware is added
        assert self.app.middleware.middlewares is None

        environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "GET"}
        _ = self.app(environ, lambda s, r: None)
        assert self.app.response.headers["Content-type"] == "text/plain"

    def test_args_not_in_path(self, bobtail_app, route_class_two):
         # Ref: https://github.com/joegasewicz/bobtail/issues/27
        routes = [
            (route_class_two, "/images/{id:int}")
        ]

        self.app = bobtail_app(routes=routes)

        # Check no middleware is added
        assert self.app.middleware.middlewares is None

        environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "GET"}
        data = self.app(environ, lambda s, r: None)
        assert data is not None

