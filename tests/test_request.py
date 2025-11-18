import pytest
import pytest_deprecate

from bobtail.wsgi import BobTail
from tests.fixtures import (
    bobtail_app,
    environ,
    multipart_data,
    form_data,
    multipart_data_with_file,
)

from bobtail.request import Request
from bobtail.headers import RequestHeaders
from bobtail.exceptions import FormDataError, MultipartFormDataError


class TestRequest:

    def test_get_path(self, bobtail_app, environ):
        class Images:
            def get(self, req, res):
                pass

        routes = [(Images(), ["/images/{id:int}"])]

        app = bobtail_app(routes=routes)

        env = environ(path="/images/1")
        data = app(env, lambda s, r: None)
        req_path = app.request.get_path()
        assert req_path == "/images/1"

        env = environ(path="/images?q=monalisa")
        data = app(env, lambda s, r: None)
        req_path = app.request.get_path()
        assert req_path == "/images?q=monalisa"

    def test_get_args(self, bobtail_app, environ):
        class Images:

            def get(self, req, res):
                pass

        routes = [
            (Images(), ["/images/{id:int}/{name:str}/{is_raining:bool}"])
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

    def test_get_args_if_key_not_present(self, bobtail_app, environ):
        class Images:

            def get(self, req, res):
                pass

        routes = [
            (Images(), ["/images/{id:int}"])
        ]

        app = bobtail_app(routes=routes)

        env = environ(path="/images/1")
        data = app(env, lambda s, r: None)
        assert app.request.get_arg("id") == 1
        assert app.request.get_arg("name") == None

        env = environ(path="/images")
        data = app(env, lambda s, r: None)
        assert app.request.get_arg("id") == None

    def test_get_json(self):
        req_headers = RequestHeaders("application/json")
        req = Request(
            query_str="",
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
            query_str="",
            path="/images",
            method="POST",
            byte_data=b'test text',
            headers=req_headers,
        )
        result = req.get_body()
        expected = 'test text'
        assert result == expected

    def test_get_params(self):
        req_headers = RequestHeaders("application/json")
        req = Request(
            query_str="name=joe&age=48",
            path="/images",
            method="GET",
            byte_data=b'test text',
            headers=req_headers,
        )
        result = req.get_params()
        expected = {"name": "joe", "age": "48"}
        assert result == expected

    @pytest.mark.parametrize(
        "query_str", ["0", "", "=", "!"]
    )
    def test_get_params_with_malformed_values(self, query_str):
        req_headers = RequestHeaders("application/json")
        req = Request(
            query_str=query_str,
            path="/images",
            method="GET",
            byte_data=b'test text',
            headers=req_headers,
        )
        result = req.get_params()
        expected = {}
        assert result == expected

    @pytest.mark.deprecated("This feature will be dropped in 0.1.0")
    def test_get_form_data(self, multipart_data):
        req_headers = RequestHeaders("application/x-www-form-urlencoded")
        req = Request(
            query_str="",
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

    @pytest.mark.deprecated("This feature will be dropped in 0.1.0")
    def test_get_multipart_data(self, multipart_data):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
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

    @pytest.mark.deprecated("This feature will be dropped in 0.1.0")
    def test_get_form_value(self, form_data):
        req_headers = RequestHeaders("application/x-www-form-urlencoded")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=form_data,
            headers=req_headers,
        )
        assert req.get_form_value("password") == "wizard"

        with pytest.raises(FormDataError):
            req.get_form_value("bananas")

    @pytest.mark.deprecated("This feature will be dropped in 0.1.0")
    def test_get_multipart_value(self, multipart_data):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data,
            headers=req_headers,
        )
        assert req.get_multipart_value("email") == "test@test.com"

        with pytest.raises(MultipartFormDataError):
            req.get_multipart_value("bananas")

    @pytest.mark.deprecated("This feature will be dropped in 0.1.0")
    def test_get_filename_value(self, multipart_data_with_file):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data_with_file,
            headers=req_headers,
        )
        assert req.get_filename_value("logo") == "bobtail.png"

        with pytest.raises(MultipartFormDataError):
            req.get_filename_value("bananas")
