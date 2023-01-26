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
            path="/images",
            method="POST",
            byte_data=form_data,
            headers=req_headers,
        )
        assert req.form.get_field("password") == "wizard"

        with pytest.raises(FormDataError):
            req.form.get_field("bananas")

class TestMultipartForm:

    def test_get_field(self):
        pass

    def test_get_file(self):
        pass

    def test_get_file_name(self):
        pass

    def test_get_file_data(self):
        pass

    def test_get_file_mimetype(self):
        pass
