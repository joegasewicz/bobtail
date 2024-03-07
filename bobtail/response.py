from typing import Dict, List, Optional
import json

from bobtail.options import BaseOptions
from bobtail.exceptions import StaticFileError
from bobtail.static_files import (
    AUDIO_FILETYPE ,
    IMAGE_FILETYPE,
    StaticFiles,
    TXT_FILETYPE,
    VIDEO_FILETYPE,
)

class Response:
    """
    The :class:`Response` object is available from within a Route method.
    """
    status: int = 200

    body: Dict = None

    html: str = None

    static: bytes = None

    options: BaseOptions

    headers: Dict = {
        "Content-Type": "application/json",
    }

    _content_length: int = None

    def __init__(self, options: BaseOptions):
        self.options = options

    def _process(self) -> List[bytes]:
        """Process final response"""
        if self.body is not None:
            resp_data = bytes(json.dumps(self.body, indent=2), "utf-8")
            self._set_content_len(resp_data)
            return [resp_data]
        if self.html is not None:
            resp_data = bytes(self.html, "utf-8")
            self._set_content_len(resp_data)
            return [resp_data]
        if self.static is not None:
            self._set_content_len(self.static)
            return [self.static]
        self._set_content_len(None)
        return []

    def _set_content_len(self, data: Optional[bytes]) -> None:
        if self._content_length is None:
            con_len = 0 if data is None else len(data)
            self.headers = {
                **self.headers,
                "Content-Length": f"{con_len}",
            }

    def set_headers(self, value: Dict) -> None:
        """
        Headers can be set from within a route method. The `Content-Type` header get
        set dynamically from :class:`Response` methods. By default, `Content-Type` is
        set to `application/json`.
        For Example::

            def get(self, req: Request, res: Response):
                res.set_headers({
                    "Content-Type": "application/json",
                })

        :param value: Excepts a dict
        """
        self.headers = {
            **self.headers,
            **value,
        }

    def set_status(self, value: int) -> None:
        """
        Set the response status.
        You can set the status with the Response object's set_status method.
        The default status is always set to 200 if there are no errors.
        For Example::

            def get(self, req: Request, res: Response):
                res.set_headers({"Content-type": "text/plain"})

        :param value: Sets the response status
        """
        self.status = value

    def set_body(self, value: Dict) -> None:
        """
        Set the body of the request.
        For example::

            def get(self, req: Request, res: Response):
                res.set_body({id: 1})

        :param value:
        """
        self.body = value

    def set_html(self, template_str: str) -> None:
        """
        Renders an HTML string. See :class:`~BaseOptions.TEMPLATE_DIR` for the
        template directory path.
        For example::

            template_str = "<h1>Hello!</h1>"

            def get(self, req: Request, res: Response):
                res.set_html(template_str)

        :param template_str:
        """
        self.set_headers({"Content-Type": "text/html"})
        self.html = template_str

    def set_static(self, path: str):
        """
        To declare a static route postfix a `*` to the route's path::

            from bobtail import BobTail AbstractRoute, BaseOptions
            from bobtail_jinja2 import BobtailJinja2

            routes = [
                (Static(), "/static/*"),
            ]

            class Options(BaseOptions):
                STATIC_DIR = "app/static"
                TEMPLATE_DIR = "app/templates"

            blog = BobTail(routes=routes, options=Options())
            blog.use(BobtailJinja2(template_dir="app/templates"))

        Calling `set_static` from within a route method will render a static
        file such as a .css, .js or a media type file. The :class:`~BaseOptions`
        class sets the `STATIC_DIR` directory.
        For example::

                class Static(AbstractRoute):
                    def get(self, req: Request, res: Response) -> None:
                        res.set_static(req.path)

        You can set the static file path using the :class:`~BaseOptions`.
        For example::

                class Options(BaseOptions):
                    STATIC_DIR = "/static"

                # Now in a route handler we can access static directory the via options
                class Static(AbstractRoute):
                    def get(self, req: Request, res: Response) -> None:
                        res.set_static(req.path)

        By default, `STATIC_DIR` is set to `/static`, if your static file is nested
        within a Python package, for example `app/static` the set as `STATIC_DIR = "app/static"`

        To render an image from within a Jinja2 template include the full path including the
        static directory name or path. For example::

            <!-- if STATIC_DIR = "/static" -->
            <body>
                <img src="/static/imgs/cat1.jpg" />
            </body>

        OR without the first forward slash::

            <body>
                <img src="static/imgs/cat1.jpg" />
            </body>

        :param path:
        """
        if len(path.split(".")) < 1:
            return None
        path_seg = path.split("/static")
        if len(path_seg) <= 1:
            return None
        path = path_seg[1]
        try:
            file_suffix = path.split("/")[-1:][0].split(".")[-1:][0]
            path = f"{self.options.STATIC_DIR}{path}"

            if file_suffix in IMAGE_FILETYPE:
                StaticFiles(self, "image").set_headers(file_suffix)
            elif file_suffix == "css":
                StaticFiles(self, "text").set_headers(file_suffix)
            elif file_suffix in VIDEO_FILETYPE:
                StaticFiles(self, "video").set_headers(file_suffix)
            elif file_suffix in AUDIO_FILETYPE:
                StaticFiles(self, "audio").set_headers(file_suffix)
            else:
                StaticFiles(self, "text").set_headers("plain")

        except Exception as exc:
            self.set_status(500)
            raise StaticFileError(
                f"Error getting filetype from static file path - {path}"
            ) from exc
        try:
            with open(path, "rb") as f:
                file_data = f.read()
                f.close()
            self.static = file_data
        except FileNotFoundError:
            self.set_status(404)
