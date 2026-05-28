import pytest

from bobtail.wsgi import Bobtail
from tests.fixtures import (
    bobtail_app,
    environ,
    multipart_data,
    form_data,
    multipart_data_with_file,
    wsgi_environ
)
from bobtail.request import Request
from bobtail.headers import RequestHeaders
from bobtail.exceptions import FormDataError, MultipartFormDataError


class TestForm:

    def test_get_field(self, form_data, wsgi_environ):
        req_headers = RequestHeaders("application/x-www-form-urlencoded")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=form_data,
            headers=req_headers,
            scheme=wsgi_environ["wsgi.url_scheme"],
            domain=wsgi_environ["SERVER_NAME"],
            port=wsgi_environ["SERVER_PORT"],
        )
        assert req.form.get_field("password") == "wizard"

        with pytest.raises(FormDataError):
            req.form.get_field("bananas")

class TestMultipartForm:

    def test_get_field(self, multipart_data, wsgi_environ):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data,
            headers=req_headers,
            scheme=wsgi_environ["wsgi.url_scheme"],
            domain=wsgi_environ["SERVER_NAME"],
            port=wsgi_environ["SERVER_PORT"],
        )
        assert req.multipart.get_field("email") == "test@test.com"

        with pytest.raises(MultipartFormDataError):
            req.multipart.get_field("bananas")

    def test_get_file(self, multipart_data_with_file, wsgi_environ):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data_with_file,
            headers=req_headers,
            scheme=wsgi_environ["wsgi.url_scheme"],
            domain=wsgi_environ["SERVER_NAME"],
            port=wsgi_environ["SERVER_PORT"],
        )
        result = req.multipart.get_file("logo")
        assert result["filename"] == "bobtail.png"
        assert result["mimetype"] == "image/png"
        assert isinstance(result["data"], bytes)


    def test_get_name(self, multipart_data_with_file, wsgi_environ):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data_with_file,
            headers=req_headers,
            scheme=wsgi_environ["wsgi.url_scheme"],
            domain=wsgi_environ["SERVER_NAME"],
            port=wsgi_environ["SERVER_PORT"],
        )
        assert req.multipart.get_name("logo") == "bobtail.png"

        with pytest.raises(MultipartFormDataError):
            req.multipart.get_name("bananas")

    def test_get_data(self, multipart_data_with_file, wsgi_environ):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data_with_file,
            headers=req_headers,
            scheme=wsgi_environ["wsgi.url_scheme"],
            domain=wsgi_environ["SERVER_NAME"],
            port=wsgi_environ["SERVER_PORT"],
        )
        result = req.multipart.get_data("logo")
        assert isinstance(result, bytes)

        with pytest.raises(MultipartFormDataError):
            req.multipart.get_data("bananas")

    def test_get_mimetype(self, multipart_data_with_file, wsgi_environ):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data_with_file,
            headers=req_headers,
            scheme=wsgi_environ["wsgi.url_scheme"],
            domain=wsgi_environ["SERVER_NAME"],
            port=wsgi_environ["SERVER_PORT"],
        )
        result = req.multipart.get_mimetype("logo")
        assert result == "image/png"

        with pytest.raises(MultipartFormDataError):
            req.multipart.get_mimetype("bananas")
