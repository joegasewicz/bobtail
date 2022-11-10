from typing import Dict, Tuple, List, Optional


class Response:

    _status: int = 200

    _body: Dict

    _data: str

    _headers: Dict = {
        "Content-Type": "application/json",
    }

    _content_length: int = None

    """
    :param value: Excepts a dict
    """
    def headers(self, value: Dict) -> None:
        self._headers = {
            **self._headers,
            **value,
        }

    """
    :param value: Sets the response status
    """
    def status(self, value: int) -> None:
        self._status = value

    """
    :param value: Set the body of the request
    """
    def body(self, value: Dict) -> None:
        self._body = value

    """
    Warning: calling this method directly inside a view handler will have no effect
    as the content length is set dynamically after the execution of the view handler
    """
    def content_len(self, data: Optional[bytes]) -> None:
        if self._content_length is None:
            con_len = 0 if data is None else len(data)
            self._headers = {
                **self._headers,
                "Content-Length": f"{con_len}",
            }
