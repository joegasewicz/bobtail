from bobtail.wsgi import BobTail


class TestRequest:

    def test_get_args(self):
        class Images:

            def get(self, req, res):
                pass

        routes = [
            (Images(), "/images/{id:int}/{name:str}/{is_raining:bool}")
        ]

        app = BobTail(routes=routes)

        environ = {"PATH_INFO": "/images/1/hello/true", "REQUEST_METHOD": "POST"}
        data = app(environ, lambda s, r: None)
        id = app.request.get_arg("id")
        name = app.request.get_arg("name")
        is_raining = app.request.get_arg("is_raining")
        assert id == 1
        assert name == "hello"
        assert is_raining is True
