import pytest


from bobtail.wsgi import BobTail


@pytest.fixture(scope="function")
def bobtail_app(routes):
    print(f"arg =====> {routes}")
    return BobTail(routes=routes)
