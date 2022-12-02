from bobtail.wsgi import BobTail
from tests.fixtures import bobtail_app, environ, multipart_data

from bobtail.request import Request
from bobtail.headers import RequestHeaders


class TestRequest:

    def test_get_args(self, bobtail_app, environ):
        class Images:

            def get(self, req, res):
                pass

        routes = [
            (Images(), "/images/{id:int}/{name:str}/{is_raining:bool}")
        ]

        app = bobtail_app(routes=routes)

        env = environ(path="/images/1/hello/true")
        data = app(env, lambda s, r: None)
        id = app.request.get_arg("id")
        name = app.request.get_arg("name")
        is_raining = app.request.get_arg("is_raining")
        assert id == 1
        assert name == "hello"
        assert is_raining is True

    def test_get_json(self):
        req_headers = RequestHeaders("application/json")
        req = Request(
            path="/images",
            method="POST",
            byte_data=b'{\n    "name": "joe"\n, "email": "joe@email.com"\n}',
            headers=req_headers,
        )
        result = req.get_json()
        expected = {"email": "joe@email.com", "name": "joe"}
        assert result == expected

    def test_get_body(self):
        req_headers = RequestHeaders("application/json")
        req = Request(
            path="/images",
            method="POST",
            byte_data=b'test text',
            headers=req_headers,
        )
        result = req.get_body()
        expected = 'test text'
        assert result == expected

    def test_get_form_data(self, multipart_data):
        req_headers = RequestHeaders("application/x-www-form-urlencoded")
        req = Request(
            path="/images",
            method="POST",
            byte_data=multipart_data,
            headers=req_headers,
        )
        result = req.get_form_data()
        expected = {
            "email": {
                "name": "email",
                "value": "test@test.com",
                "type": "text",
            },
            "password": {
                "name": "password",
                "value": "wizard",
                "type": "text",
            },
        }
        assert result == expected

    def test_get_multipart_data(self, multipart_data):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            path="/images",
            method="POST",
            byte_data=multipart_data,
            headers=req_headers,
        )
        result = req.get_multipart_data()
        expected = {
            "email": {
                "name": "email",
                "value": "test@test.com",
                "type": "text",
            },
            "password": {
                "name": "password",
                "value": "wizard",
                "type": "text",
            },
        }
        assert result == expected


