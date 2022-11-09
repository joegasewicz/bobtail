from typing import List, Tuple


class NoRoutesError(Exception):
    message = "Expected a list of routes"


class BobTail:

    routes: List[Tuple[object, str]]

    def __init__(self, *args, **kwargs):
        if "routes" not in kwargs:
            raise NoRoutesError("Expected a list of routes")
        self.routes = kwargs["routes"]

    def __call__(self, environ, start_response):

        current_path = environ["PATH_INFO"]
        current_method = environ["REQUEST_METHOD"]

        for route in self.routes:
            if route[1] == current_path:
                match current_method:
                    case "GET":
                        pass
                    case "POST":
                        pass
                    case "DELETE":
                        pass
                    case "PUT":
                        pass

        # print(f"here---> {environ}")
        status = "200 OK"
        response_headers = [("Content-type", "text/plain")]
        start_response(status, response_headers)
        return [b"Hello World!\n"]
