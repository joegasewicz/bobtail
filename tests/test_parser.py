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
            (Images1(), "/images/image/{id:int}"),
            (Videos1(), "/videos/movie/{name:string}"),
            (Files1(), "/files/new/{true:bool}"),
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
            (Images2(), "/images/image/{id:int}/pic/{file_name:str}"),
            (Videos2(), "/videos/movie/{name:str}"),
            (Files2(), "/files/new/{true:bool}"),
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
            (Images3(), "/images"),
            (Home3(), "/"),
            (Files3(), "/"),
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
