from bobtail.wsgi import BobTail


def test_headers():
    class Images:

        def get(self, req, res):
            res.set_headers({"Content-type": "text/plain"})
            res.set_status(200)
            res.set_body({})

    routes = [
        (Images(), "/images")
    ]


    app = BobTail(routes=routes)

    app.use(lambda e: None)

    environ = {"PATH_INFO": "/images", "REQUEST_METHOD": "GET"}
    _ = app(environ, lambda s, r: None)
    assert app.response.headers["Content-type"] == "text/plain"