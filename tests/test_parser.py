from bobtail.parser import Parser
from bobtail.route import AbstractRoute


class TestParser:

    def test_route(self):
        class Images:
            def get(self, req, res):
                pass

        class Videos:
            def get(self, req, res):
                pass

        class Files:
            def get(self, req, res):
                pass

        routes = [
            (Images(), "/images/image/{id:int}"),
            (Videos(), "/videos/movie/{name:string}"),
            (Files(), "/files/new/{true:bool}"),
        ]

        p = Parser(routes)
        path = "/images/image/1"
        result = p.route(path)
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
            'class': 'Files'
        }
        assert result == expected

    def test_route_with_multiple_vars(self):
        class Images:
            def get(self, req, res):
                pass

        class Videos:
            def get(self, req, res):
                pass

        class Files:
            def get(self, req, res):
                pass

        routes = [
            (Images(), "/images/image/{id:int}/pic/{file_name:str}"),
            (Videos(), "/videos/movie/{name:str}"),
            (Files(), "/files/new/{true:bool}"),
        ]

        p = Parser(routes)
        path = "/images/image/1/pic/sunny.png"
        result = p.route(path)
        expected = {
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
            'class': 'Files'
        }
        assert result == expected
