from typing import List, Tuple, Dict, Optional
from abc import ABC, abstractmethod
import json

from bobtail.response import Response
from bobtail.request import Request
from bobtail.status import Status


class AbstractRoute(ABC):

    @abstractmethod
    def get(self, req: Request, res: Response):
        pass

    @abstractmethod
    def post(self, req: Request, res: Response):
        pass

    @abstractmethod
    def put(self, req: Request, res: Response):
        pass

    @abstractmethod
    def delete(self, req: Request, res: Response):
        pass


class BobTail:

    environ: Dict

    routes: List[Tuple[AbstractRoute, str]]

    response: Response

    request: Request

    _status: Status

    def _handle_404(self):
        self.response.set_status(404)

    def __init__(self, *args, **kwargs):
        if "routes" not in kwargs:
            raise NoRoutesError("Expected a list of routes")
        self.routes = kwargs["routes"]

    def init_response(self):
        self.response = Response()

    def set_request(self):
        self.request = Request(
            path=self.environ["PATH_INFO"],
            method=self.environ["REQUEST_METHOD"],
        )

    def _call_handler(self, route: callable, method: str):
        if hasattr(route,  method):
            try:
                handler = getattr(route, method)
                if not handler:
                    self._handle_404()
                    return
                handler(self.request, self.response)
            except Exception as exc:
                raise RouteClassError("route class is not instantiated") from exc
        else:
            self._handle_404()

    def _handle_route(self):
        for current_route in self.routes:
            route, curr_path = current_route
            if curr_path == self.request.path:
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
        self._handle_404()

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
