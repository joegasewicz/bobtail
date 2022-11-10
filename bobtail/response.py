from typing import Dict, Tuple, List, Optional
import json


class Response:

    status: int = 200

    body: Dict = None

    headers: Dict = {
        "Content-Type": "application/json",
    }

    _content_length: int = None

    """
    :param value: Excepts a dict
    """
    def set_headers(self, value: Dict) -> None:
        self.headers = {
            **self.headers,
            **value,
        }

    """
    :param value: Sets the response status
    """
    def set_status(self, value: int) -> None:
        self.status = value

    """
    :param value: Set the body of the request
    """
    def set_body(self, value: Dict) -> None:
        self.body = value

    """
    Warning: calling this method directly inside a route handler will have no effect
    as the content length is set dynamically after the execution of the route handler
    """
    def content_len(self, data: Optional[bytes]) -> None:
        if self._content_length is None:
            con_len = 0 if data is None else len(data)
            self.headers = {
                **self.headers,
                "Content-Length": f"{con_len}",
            }

    def _process(self) -> List[bytes]:
        """Process final response"""
        if self.body is not None:
            resp_data = bytes(json.dumps(self.body, indent=2), "utf-8")
            self.content_len(resp_data)
            return [resp_data]
        self.content_len(None)
        return []
