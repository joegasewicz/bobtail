from bobtail.response import Response


class TestResponse:

    def test_headers(self):
        headers = {"Content-Type": "text/plain"}
        r = Response()
        r.headers(headers)
        assert r._headers == headers

    def test_status(self):
        status = 404
        r = Response()
        r.status(status)
        assert r._status == status

    def test_body(self):
        json_data = {"id": 1}
        r = Response()
        r.body(json_data)
        assert r._body == json_data

    def test_content_len(self):
        byte_data = b"hello, world!"
        r = Response()
        r.content_len(byte_data)
        expected = {
            "Content-Type": "application/json",
            "Content-Length": f"{len(byte_data)}",
        }
        assert expected == r._headers
