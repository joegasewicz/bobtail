import pytest
import io


from bobtail.wsgi import BobTail


@pytest.fixture(scope="function")
def bobtail_app():
    def inner(*, routes):
        return BobTail(routes=routes)
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
    def inner(*, path="/images", method="GET", data=b'{\n    "name": "joe"\n}', content="text/plain"):
        return {
            "PATH_INFO": path,
            "REQUEST_METHOD": method,
            "wsgi.input": io.BytesIO(data),
            "CONTENT_TYPE": content,
        }

    return inner


@pytest.fixture(scope="function")
def multipart_data():
    return b'----------------------------782797925953098016952108\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\ntest@test.com\r\n----------------------------782797925953098016952108\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nwizard\r\n----------------------------782797925953098016952108--\r\n'
