from typing import List, Dict

from bobtail.response import Response
from bobtail.request import Request
from bobtail.status import Status
from bobtail.exceptions import NoRoutesError, RouteClassError
from bobtail.route import Route, Handler
from bobtail.parser import Parser
from bobtail.middleware import Middleware
from bobtail.headers import ResponseHeaders, RequestHeaders
from bobtail.options import BaseOptions
from bobtail.middleware import AbstractMiddleware


class BobTail:
    """
    :kwargs:
    :key routes: A tuple list of :class:`~AbstractRoute` & request path
    """
    #: Bobtail is a micro http web framework.
    environ: Dict

    #: Routes is a list of tuple :class:`~AbstractRoute` & request path pairs.
    #: For Example::
    #:
    #:  routes = [
    #:      (Images(), "/images")
    #:  ]
    #:
    routes: List[Route]

    #: Options (Optional). See :class:`~BaseOptions` for option list. Base options
    #: can be overridden & or set on a concrete BaseOptions instance.
    #: For Example::
    #:
    #:  from bobtail.options import BaseOptions
    #:
    #:  class Options(BaseOptions):
    #:      PORT = 8000                     # set by default
    #:      STATIC_DIR = "app/static"       # set by default
    #:      TEMPLATE_DIR = "app/templates"  # set by default
    #:
    #:  app = Bobtail(Options, routes=[])
    #:
    options: BaseOptions

    response: Response = None

    request: Request

    _status: Status

    _body: str

    parse_metadata: Dict = None

    middleware: Middleware = None

    request_headers: RequestHeaders

    response_headers: ResponseHeaders

    def __init__(self, *args, **kwargs):
        if "routes" not in kwargs:
            raise NoRoutesError("Expected a list of routes")
        self.routes = kwargs["routes"]
        _options = kwargs.get("options")
        if _options:
            self.options = _options
        else:
            class DefaultOptions(BaseOptions):
                pass

            self.options = DefaultOptions()
        self.middleware = Middleware()

    def _handle_404(self, req: Request, res: Response):
        self.response.set_status(404)

    def _init_response(self):
        self.response = Response(self.options)

    def _set_request(self):
        self.request = Request(
            path=self.environ["PATH_INFO"],
            method=self.environ["REQUEST_METHOD"],
            byte_data=self.environ["wsgi.input"].read(),
            headers=RequestHeaders(content_type=self.environ.get("CONTENT_TYPE")),
            query_str=self.environ["QUERY_STRING"]
        )

    def _call_handler(self, route: callable, method: str):
        if hasattr(route,  method):
            handler: Handler = getattr(route, method)
            if not handler:
                self.middleware.call(self.request, self.response, self._handle_404)
                return
            self.middleware.call(self.request, self.response, handler)
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
        self._set_request()
        self._init_response()
        # Call route handler with default response
        self._handle_route()

        self._status = Status()
        status = self._status.get(self.response.status)

        response_headers = []

        for k, v in self.response.headers.items():
            t = (k, v,)
            response_headers.insert(0, t)

        # Start response
        start_response(status, response_headers)
        # Process the final byte list & headers
        data = self.response._process()
        # clean up text/html string
        return data

    def use(self, middleware: AbstractMiddleware):
        """
        Enables using third party middleware.
        For example::

            from bobttail_logger import BobtailLogger

            app = Bobtail(routes=routes)

            # Here we are using `bobtail-logger` logging middleware
            app.use(BobtailLogger())

        Creating custom middleware example.
        A Middleware object must implement :class:`AbstractMiddleware`.
        For example::

            from bobtail import Request, Response
            from bobtail.middleware import AbstractMiddleware, Tail

            class BobtailCors(AbstractMiddleware):

                def run(self, req: Request, res: Response, tail: Tail) -> None:
                    res.set_headers({
                        "Access-Control-Allow-Origin": "*",
                    })
                    tail(req, res)

        :param middleware: :class:`AbstractMiddleware`
        :return: None
        """
        self.middleware.add(middleware)
