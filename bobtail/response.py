from typing import Dict, List, Optional
import json


class Response:
    """
    The :class:`Response` object is available from within a Route method.
    """
    status: int = 200

    body: Dict = None

    html: str = None

    static: bytes = None

    headers: Dict = {
        "Content-Type": "application/json",
    }

    _content_length: int = None

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
        Renders an HTML string.
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
        Calling `set_status` from within a route method will render a static
        file such as a .css, .js or a media type file. The :class:`~BaseOptions`
        class sets the `STATIC_DIR` directory.
        For example::

                def get(self, req: Request, res: Response) -> None:
                    res.set_static("cat1.jpg")

        :param path:
        """
        self.set_headers({"Content-Type": "image/jpeg"})
        file = open(path, "rb")
        file_data = file.read()
        file.close()
        self.static = file_data
