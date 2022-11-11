import pytest


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

        def init(self, req, res, tail) -> None:
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

        def init(self, req, res, tail) -> None:
            res.set_headers({
                "Access-Control-Allow-Origin": "*",
            })
            tail(req, res)
    return MockLogger()
