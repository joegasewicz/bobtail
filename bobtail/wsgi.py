from typing import List, Tuple, Dict

from bobtail.response import Response
from bobtail.request import Request
from bobtail.status import Status
from bobtail.exceptions import NoRoutesError, RouteClassError
from bobtail.route import Route, Handler
from bobtail.parser import Parser
from bobtail.middleware import Middleware
from bobtail.headers import ResponseHeaders, RequestHeaders
from bobtail.wsgi_input import WSGIInput


class BobTail:

    environ: Dict

    routes: List[Route]

    response: Response = None

    request: Request

    _status: Status

    _body: str

    parse_metadata: Dict = None

    middleware: Middleware = None

    request_headers: RequestHeaders

    response_headers: ResponseHeaders

    def _handle_404(self, req: Request, res: Response):
        self.response.set_status(404)

    def __init__(self, *args, **kwargs):
        if "routes" not in kwargs:
            raise NoRoutesError("Expected a list of routes")
        self.routes = kwargs["routes"]
        self.middleware = Middleware()

    def init_response(self):
        self.response = Response()

    def set_request(self):
        self.request = Request(
            path=self.environ["PATH_INFO"],
            method=self.environ["REQUEST_METHOD"],
            byte_data=self.environ["wsgi.input"].read(),
            headers=RequestHeaders(content_type=self.environ["CONTENT_TYPE"]),
        )

    def _call_handler(self, route: callable, method: str):
        if hasattr(route,  method):
            try:
                handler: Handler = getattr(route, method)
                if not handler:
                    self.middleware.call(self.request, self.response, self._handle_404)
                    return
                self.middleware.call(self.request, self.response, handler)
            except Exception as exc:
                raise RouteClassError("route class is not instantiated") from exc
        else:
            self.middleware.call(self.request, self.response, self._handle_404)

    def _handle_route(self):
        p = Parser(self.routes, self.request.path)
        self.parse_metadata = p.route()
        # Set the args on the request object
        if self.parse_metadata and "vars" in self.parse_metadata:
            self.request.set_args(self.parse_metadata["vars"])
        for current_route in self.routes:
            route, _ = current_route
            if route.__class__.__name__ == p.get_matched():
                match self.request.method:
                    case "GET":
                        self._call_handler(route, "get")
                        return
                    case "POST":
                        self._call_handler(route, "post")
                        return
                    case "DELETE":
                        self._call_handler(route, "delete")
                        return
                    case "PUT":
                        self._call_handler(route, "put")
                        return
                    case "PATCH":
                        self._call_handler(route, "patch")
                        return
        self.middleware.call(self.request, self.response, self._handle_404)

    def __call__(self, environ, start_response):
        self.environ = environ

        # Set request & response
        self.set_request()
        self.init_response()
        # Call route handler with default response
        self._handle_route()

        self._status = Status()
        status = self._status.get(self.response.status)

        response_headers = [("Content-type", "application/json")]

        # Start response
        start_response(status, response_headers)
        # Process the final byte list & headers
        data = self.response._process()
        return data

    def use(self, middleware):
        self.middleware.add(middleware)
