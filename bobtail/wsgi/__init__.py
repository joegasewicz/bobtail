from typing import List, Tuple
from abc import ABC, abstractmethod


class AbstractRoute(ABC):

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def post(self):
        pass

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def patch(self):
        pass


class NoRoutesError(Exception):
    message = "Expected a list of routes"


class BobTail:

    routes: List[Tuple[AbstractRoute, str]]

    def __init__(self, *args, **kwargs):
        if "routes" not in kwargs:
            raise NoRoutesError("Expected a list of routes")
        self.routes = kwargs["routes"]

    def __call__(self, environ, start_response):

        current_path = environ["PATH_INFO"]
        current_method = environ["REQUEST_METHOD"]

        for r in self.routes:
            route, curr_path = r
            if curr_path == current_path:
                match current_method:
                    case "GET":
                        route.get()
                    case "POST":
                        route.post()
                    case "DELETE":
                        route.delete()
                    case "PUT":
                        route.put()
                    case "PATCH":
                        route.patch()

        status = "200 OK"
        response_headers = [("Content-type", "text/plain")]
        start_response(status, response_headers)
        return [b"Hello World!\n"]
