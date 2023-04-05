import pytest
import io


from bobtail.wsgi import BobTail
from bobtail.options import BaseOptions


@pytest.fixture(scope="function")
def bobtail_app():
    class _Options(BaseOptions):
        pass
    def inner(*, routes):
        return BobTail(routes=routes, options=_Options)
    return inner


@pytest.fixture(scope="function")
def route_class_one():
    class TestOne:

        def get(self, req, res):
            res.set_body({"users": [{"id": 1}, {"id": 2}]})
            res.set_status(200)

        def post(self, req, res):
            res.set_body(None)
            res.set_status(202)

        def delete(self, req, res):
            res.set_body(None)
            res.set_status(201)

        def put(self, req, res):
            res.set_body({"id": 1})
            res.set_status(202)

        def patch(self, req, res):
            res.set_body({"id": 1})
            res.set_status(202)
    return TestOne()


@pytest.fixture(scope="function")
def route_class_two():
    class TestTwo:
        def get(self, req, res):
            res.set_headers({"Content-type": "text/plain"})
            res.set_status(200)
            res.set_body({})
    return TestTwo()


@pytest.fixture(scope="function")
def middle_cors():
    class MockCors:
        def __init__(self):
            pass

        def run(self, req, res, tail) -> None:
            res.set_headers({
                "Access-Control-Allow-Origin": "*",
            })
            tail(req, res)
    return MockCors()


@pytest.fixture(scope="function")
def middle_logger():
    class MockLogger:
        def __init__(self):
            pass

        def run(self, req, res, tail) -> None:
            res.set_headers({
                "Access-Control-Allow-Origin": "*",
            })
            tail(req, res)
    return MockLogger()


@pytest.fixture(scope="function")
def environ():
    def inner(*, path="/images", method="GET", data=b'{\n    "name": "joe"\n}', content="text/plain", query_str = ""):
        return {
            "PATH_INFO": path,
            "REQUEST_METHOD": method,
            "wsgi.input": io.BytesIO(data),
            "CONTENT_TYPE": content,
            "QUERY_STRING": query_str,
        }

    return inner


@pytest.fixture(scope="function")
def multipart_data():
    return b'----------------------------782797925953098016952108\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\ntest@test.com\r\n----------------------------782797925953098016952108\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nwizard\r\n----------------------------782797925953098016952108--\r\n'


@pytest.fixture(scope="function")
def multipart_data_with_file():
    return b'----------------------------138321988060416233833146\r\nContent-Disposition: form-data; name="name"\r\n\r\nJoe\r\n----------------------------138321988060416233833146\r\nContent-Disposition: form-data; name="age"\r\n\r\n47\r\n----------------------------138321988060416233833146\r\nContent-Disposition: form-data; name="logo"; filename="bobtail.png"\r\nContent-Type: image/png\r\n\r\n\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x08e\x00\x00\x02\x04\x08\x06\x00\x00\x01\xcd\x8f1\xca\x00\x00\x00\\x12\xbf\xb4}\xae\xc6n\xee\xc8\xe7\xee(aFB\xfb%Fn\xbe\x90[3cj\xc9\x02R\xea\x94\x80\x12P\x02J@\t(\x01%\xa0\x04\x94\x80\x12h\x08\x81\xff\x01\t\xb6!\x1f\x86\xa9?\xfb\x00\x00\x00\x00IEND\xaeB`\x82\r\n----------------------------138321988060416233833146--\r\n'


@pytest.fixture(scope="function")
def form_data():
    return b'----------------------------782797925953098016952108\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\ntest@test.com\r\n----------------------------782797925953098016952108\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nwizard\r\n----------------------------782797925953098016952108--\r\n'


@pytest.fixture(scope="function")
def default_options():
    class _Options(BaseOptions):
        pass
    return _Options()