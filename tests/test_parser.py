import pytest

from bobtail.parser import Parser
from bobtail.route import AbstractRoute


class TestParser:

    def test_route(self):
        class Images1:
            def get(self, req, res):
                pass

        class Videos1:
            def get(self, req, res):
                pass

        class Files1:
            def get(self, req, res):
                pass

        routes1 = [
            (Images1(), ["/images/image/{id:int}"]),
            (Videos1(), ["/videos/movie/{name:string}"]),
            (Files1(), ["/files/new/{true:bool}"]),
        ]
        path1 = "/images/image/1"
        p1 = Parser(routes1, path1)
        result = p1.route()
        expected = {
            'route': '/images/image/{id:int}',
            'split': ['images', 'image', '{id:int}'],
            'vars': {
                'id': {
                    'name': 'id',
                    'type': 'int',
                    'value': '1',
                }
            },
            'path': '/images/image/1',
            'class': 'Images1'
        }
        assert result == expected

    def test_route_with_multiple_vars(self):
        class Images2:
            def get(self, req, res):
                pass

        class Videos2:
            def get(self, req, res):
                pass

        class Files2:
            def get(self, req, res):
                pass

        routes2 = [
            (Images2(), ["/images/image/{id:int}/pic/{file_name:str}"]),
            (Videos2(), ["/videos/movie/{name:str}"]),
            (Files2(), ["/files/new/{true:bool}"]),
        ]
        path2 = "/images/image/1/pic/sunny.png"
        p2 = Parser(routes2, path2)
        result2 = p2.route()
        expected2 = {
            'route': '/images/image/{id:int}/pic/{file_name:str}',
            'split': ['images', 'image', '{id:int}', 'pic', '{file_name:str}'],
            'vars': {
                'id': {
                    'name': 'id',
                    'type': 'int',
                    'value': '1',
                },
                'file_name': {
                    'name': 'file_name',
                    'type': 'str',
                    'value': 'sunny.png',
                }
            },
            'path': '/images/image/1/pic/sunny.png',
            'class': 'Images2'
        }
        assert result2 == expected2

    def test_route_index_route(self):
        class Home3:
            def get(self, req, res):
                pass

        class Images3:
            def get(self, req, res):
                pass

        class Files3:
            def get(self, req, res):
                pass

        routes3 = [
            (Images3(), ["/images"]),
            (Home3(), ["/"]),
            (Files3(), ["/"]),
        ]
        path = "/"
        p3 = Parser(routes3, path)
        result = p3.route()
        expected = {
            'class': 'Home3',
            'path': '/',
            'route': '/',
            'split': [''],
            'vars': None,
        }
        assert result == expected

    def test_extra_segments(self):
        class Images6:
            def get(self, req, res):
                pass

        class Videos6:
            def get(self, req, res):
                pass

        class Files6:
            def get(self, req, res):
                pass

        routes2 = [
            (Images6(), ["/images/image/{id:int}/pic/{file_name:str}"]),
            (Videos6(), ["/videos/movie/{name:str}"]),
            (Files6(), ["/files/new/{true:bool}"]),
        ]
        path2 = "/images/image/1/pic/sunny.png/hello!"
        p2 = Parser(routes2, path2)
        _ = p2.route()
        assert p2.meta_data["matched"] is None

    def test_get_matched(self):
        class Home4:
            def get(self, req, res):
                pass

        class Images4:
            def get(self, req, res):
                pass

        class Files4:
            def get(self, req, res):
                pass

        routes4 = [
            (Images4(), ["/images"]),
            (Home4(), ["/"]),
            (Files4(), ["/"]),
        ]
        path = "/"
        p4 = Parser(routes4, path)
        result = p4.route()
        expected = {
            'class': 'Home4',
            'path': '/',
            'route': '/',
            'split': [''],
            'vars': None,
        }
        assert result == expected
        m = p4.get_matched()
        assert m == "Home4"

    def test_static_route(self):
        class Images6:
            def get(self, req, res):
                pass

        class Videos6:
            def get(self, req, res):
                pass

        class Files6:
            def get(self, req, res):
                pass

        routes2 = [
            (Videos6(), ["/videos"]),
            (Files6(), ["/files/new/{true:bool}"]),
            (Images6(), ["/static/*"]),
        ]
        path2 = "/static/images/sunny.png"
        p2 = Parser(routes2, path2)
        _ = p2.route()
        assert p2.meta_data["matched"] == "Images6"

    @pytest.mark.parametrize(
        "mock_path,matched", [
            ("/products", "Product"),
            ("/roducts", None),
            ("/products/1", "Product"),
            ("/roducts/1", None),
            ("/products/1/details", "Product"),
            ("/products/1/details/2", "Product"),

        ]
    )
    def test_all_segments_of_a_complex_path(self, mock_path, matched):
        class Product:
            def get(self, req, res):
                res.set_body({"product": "coffee"})

        class Images6:
            def get(self, req, res):
                pass

        class Videos6:
            def get(self, req, res):
                pass

        class Files6:
            def get(self, req, res):
                pass

        routes = [
            (Videos6(), ["/videos"]),
            (Files6(), ["/files/new/{true:bool}"]),
            (Product(), [
                "/products/{product_id:int}/details",
                "/products/{product_id:int}",
                "/products",
                "/products/{product_id:int}/details/{detail_is:int}",
            ]),
            (Images6(), ["/static/*"]),
        ]
        p = Parser(routes, mock_path)
        _ = p.route()

        assert p.meta_data["matched"] == matched
