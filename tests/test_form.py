import pytest

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


class TestForm:

    def test_get_field(self, form_data):
        req_headers = RequestHeaders("application/x-www-form-urlencoded")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=form_data,
            headers=req_headers,
        )
        assert req.form.get_field("password") == "wizard"

        with pytest.raises(FormDataError):
            req.form.get_field("bananas")

class TestMultipartForm:

    def test_get_field(self, multipart_data):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data,
            headers=req_headers,
        )
        assert req.multipart.get_field("email") == "test@test.com"

        with pytest.raises(MultipartFormDataError):
            req.multipart.get_field("bananas")

    def test_get_file(self, multipart_data_with_file):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data_with_file,
            headers=req_headers,
        )
        result = req.multipart.get_file("logo")
        assert result["filename"] == "bobtail.png"
        assert result["mimetype"] == "image/png"
        assert isinstance(result["data"], bytes)


    def test_get_name(self, multipart_data_with_file):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data_with_file,
            headers=req_headers,
        )
        assert req.multipart.get_name("logo") == "bobtail.png"

        with pytest.raises(MultipartFormDataError):
            req.multipart.get_name("bananas")

    def test_get_data(self, multipart_data_with_file):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data_with_file,
            headers=req_headers,
        )
        result = req.multipart.get_data("logo")
        assert isinstance(result, bytes)

        with pytest.raises(MultipartFormDataError):
            req.multipart.get_data("bananas")

    def test_get_mimetype(self, multipart_data_with_file):
        req_headers = RequestHeaders("multipart/form-data")
        req = Request(
            query_str="",
            path="/images",
            method="POST",
            byte_data=multipart_data_with_file,
            headers=req_headers,
        )
        result = req.multipart.get_mimetype("logo")
        assert result == "image/png"

        with pytest.raises(MultipartFormDataError):
            req.multipart.get_mimetype("bananas")
