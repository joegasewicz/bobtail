from bobtail.response import Response
from bobtail.options import BaseOptions
from tests.fixtures import default_options


class TestResponse:

    def test_headers(self, default_options):
        headers = {"Content-Type": "text/plain"}
        r = Response(default_options)
        r.set_headers(headers)
        assert r.headers == headers

    def test_status(self, default_options):
        status = 404
        r = Response(default_options)
        r.set_status(status)
        assert r.status == status

    def test_body(self, default_options):
        json_data = {"id": 1}
        r = Response(default_options)
        r.set_body(json_data)
        assert r.body == json_data

    def test_content_len(self, default_options):
        byte_data = b"hello, world!"
        r = Response(default_options)
        r._set_content_len(byte_data)
        expected = {
            "Content-Type": "application/json",
            "Content-Length": f"{len(byte_data)}",
        }
        assert expected == r.headers

    def test_set_html(self, default_options):
        r = Response(default_options)
        r.set_html("hello world")
        assert r.html == "hello world"
        assert r.headers == {'Content-Type': 'text/html'}

    def test_set_static(self, default_options):
        class _Option(BaseOptions):
            STATIC_DIR = "tests/static"
        r = Response(_Option())
        fp = "tests/static/img/cat1.jpg"
        r.set_static(fp)
        assert isinstance(r.static, bytes)
