from typing import List, Tuple, Dict, Optional
from abc import ABC, abstractmethod

from bobtail.response import Response
from bobtail.request import Request


class AbstractRoute(ABC):

    @abstractmethod
    def get(self, req: Request) -> Tuple[Optional[Dict], int]:
        pass

    @abstractmethod
    def post(self, req: Request) -> Tuple[Optional[Dict], int]:
        pass

    @abstractmethod
    def put(self, req: Request) -> Tuple[Optional[Dict], int]:
        pass

    @abstractmethod
    def delete(self, req: Request) -> Tuple[Optional[Dict], int]:
        pass

    @abstractmethod
    def patch(self, req: Request) -> Tuple[Optional[Dict], int]:
        pass


class NoRoutesError(Exception):
    pass


class RouteClassError(Exception):
    pass


class BobTail:

    environ: Dict

    routes: List[Tuple[AbstractRoute, str]]

    response: Response

    request: Request

    def _handle_404(self) -> Tuple[Optional[Dict], int]:
        return None, 404

    def __init__(self, *args, **kwargs):
        if "routes" not in kwargs:
            raise NoRoutesError("Expected a list of routes")
        self.routes = kwargs["routes"]

    def set_response(self, data, route_status):
        self.response = Response(data, route_status)

    def set_request(self):
        self.request = Request(
            path=self.environ["PATH_INFO"],
            method=self.environ["REQUEST_METHOD"],
        )

    def _handle_route(self, request: Request):
        for r in self.routes:
            route, curr_path = r
            if curr_path == request.path:
                match request.method:
                    case "GET":
                        if hasattr(route, "get"):
                            try:
                                return route.get(request)
                            except TypeError:
                                raise RouteClassError("route class is not instantiated")
                        else:
                            return self._handle_404()
                    case "POST":
                        if hasattr(route, "post"):
                            try:
                                return route.post(request)
                            except TypeError:
                                raise RouteClassError("route class is not instantiated")
                        else:
                            return self._handle_404()
                    case "DELETE":
                        if hasattr(route, "delete"):
                            try:
                                return route.delete(request)
                            except TypeError:
                                raise RouteClassError("route class is not instantiated")
                        else:
                            return self._handle_404()
                    case "PUT":
                        if hasattr(route, "put"):
                            try:
                                return route.put(request)
                            except TypeError:
                                raise RouteClassError("route class is not instantiated")
                        else:
                            return self._handle_404()
                    case "PATCH":
                        if hasattr(route, "patch"):
                            try:
                                return route.patch(request)
                            except TypeError:
                                raise RouteClassError("route class is not instantiated")
                        else:
                            return self._handle_404()

    def __call__(self, environ, start_response):
        self.environ = environ
        self.set_request()
        data, route_status = self._handle_route(self.request)
        self.set_response(data, route_status)
        status = f"{self.response.status} OK"
        response_headers = [("Content-type", "text/plain")]
        start_response(status, response_headers)
        byte_data: bytes
        if data is not None:
            return [bytes(str(data), "utf-8")]
        return None
