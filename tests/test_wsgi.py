import pytest

from tests.fixtures import bobtail_app
from tests.fixtures import (
    route_class_one,
    route_class_two,
    middle_cors,
    middle_logger,
    environ,
)

from bobtail.wsgi import BobTail


class TestBobtail:

    app: BobTail = None

    def teardown_method(self):
        self.app = None

    def test_use(self, bobtail_app, middle_cors, middle_logger, environ):
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

        env = environ()
        _ = self.app(env, lambda s, r: None)
        assert self.app.response.headers["Access-Control-Allow-Origin"] == "*"

    def test_handlers_get(self, bobtail_app, route_class_one, environ):

        routes = [
            (route_class_one, ["/images"])
        ]
        self.app = bobtail_app(routes=routes)

        # GET
        env = environ()
        data = self.app(env, lambda s, r: None)
        assert self.app.response.body == {"users": [{"id": 1}, {"id": 2}]}
        assert self.app.response.status == 200
        assert data == [b'{\n  "users": [\n    {\n      "id": 1\n    },\n    {\n      "id": 2\n    }\n' b'  ]\n}']
        # Check no middleware is added
        assert self.app.middleware.middlewares is None

    def test_handlers_post(self, bobtail_app, route_class_one, environ):
        routes = [
            (route_class_one, ["/images"])
        ]

        self.app = bobtail_app(routes=routes)

        # POST
        env = environ(method="POST")

        data = self.app(env, lambda s, r: None)

        assert data == []
        assert self.app.response.body is None
        assert self.app.response.status == 202
        # Check no middleware is added
        assert self.app.middleware.middlewares is None

    def test_handlers_delete(self, bobtail_app, route_class_one, environ):
        routes = [
            (route_class_one, ["/images"])
        ]
        self.app = bobtail_app(routes=routes)

        # # DELETE
        env = environ(method="DELETE")
        data = self.app(env, lambda s, r: None)
        assert data == []
        assert self.app.response.body is None
        assert self.app.response.status == 201
        # Check no middleware is added
        assert self.app.middleware.middlewares is None

    def test_handlers_put(self, bobtail_app, route_class_one, environ):
        routes = [
            (route_class_one, ["/images"])
        ]
        self.app = bobtail_app(routes=routes)

        # PUT
        env = environ(method="PUT")
        data = self.app(env, lambda s, r: None)
        assert data == [b'{\n  "id": 1\n}']
        assert self.app.response.body == {"id": 1}
        assert self.app.response.status == 202
        # Check no middleware is added
        assert self.app.middleware.middlewares is None

    def test_handlers_path(self, bobtail_app, route_class_one, environ):
        routes = [
            (route_class_one, ["/images"])
        ]
        self.app = bobtail_app(routes=routes)

        # PATCH
        env = environ(method="PATCH", query_str="name=joe&age=48")
        data = self.app(env, lambda s, r: None)
        assert data == [b'{\n  "id": 1\n}']
        assert self.app.response.body == {"id": 1}
        assert self.app.response.status == 202
        assert self.app.request.get_params() == {"name": "joe", "age": "48"}

        # Check no middleware is added
        assert self.app.middleware.middlewares is None

    def test_headers(self, bobtail_app, route_class_two, environ):

        routes = [
            (route_class_two, ["/images"])
        ]

        self.app = bobtail_app(routes=routes)

        # Check no middleware is added
        assert self.app.middleware.middlewares is None

        env = environ()
        _ = self.app(env, lambda s, r: None)
        assert self.app.response.headers["Content-type"] == "text/plain"

    def test_args_not_in_path(self, bobtail_app, route_class_two, environ):
         # Ref: https://github.com/joegasewicz/bobtail/issues/27
        routes = [
            (route_class_two, ["/images/{id:int}"])
        ]

        self.app = bobtail_app(routes=routes)

        # Check no middleware is added
        assert self.app.middleware.middlewares is None

        env = environ()
        data = self.app(env, lambda s, r: None)
        assert data is not None

    def test_no_options(self, environ):
        self.app = BobTail(routes=[])
        env = environ()
        try:
            _ = self.app(env, lambda s, r: None)
        except AttributeError:
            pytest.fail("Default options are not set!")

        assert self.app.options.PORT == 8000
        assert self.app.options.STATIC_DIR is "static"
        assert self.app.options.TEMPLATE_DIR is "templates"

