from typing import Dict, Tuple, List, Optional, Self
import json

from bobtail.request import Request


class Response:
    status: int = 200

    body: Dict = None

    headers: Dict = {
        "Content-Type": "application/json",
    }

    _content_length: int = None

    def _process(self) -> List[bytes]:
        """Process final response"""
        if self.body is not None:
            resp_data = bytes(json.dumps(self.body, indent=2), "utf-8")
            self.set_content_len(resp_data)
            return [resp_data]
        self.set_content_len(None)
        return []

    def set_content_len(self, data: Optional[bytes]) -> None:
        """
        Warning: calling this method directly inside a route handler will have no effect
        as the content length is set dynamically after the execution of the route handler
        :param data:
        :type data:
        :return:
        :rtype:
        """
        if self._content_length is None:
            con_len = 0 if data is None else len(data)
            self.headers = {
                **self.headers,
                "Content-Length": f"{con_len}",
            }

    def set_headers(self, value: Dict) -> None:
        """

        :param value: Excepts a dict
        :type value:
        :return:
        :rtype:
        """
        self.headers = {
            **self.headers,
            **value,
        }

    def set_status(self, value: int) -> None:
        """
        :param value: Sets the response status
        :type value:
        :return:
        :rtype:
        """
        self.status = value

    def set_body(self, value: Dict) -> None:
        """
        Set the body of the request
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.body = value
