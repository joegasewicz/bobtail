from typing import Dict, Union
from abc import ABC

from bobtail.wsgi_input import WSGIInput
from bobtail.headers import RequestHeaders


class Request(ABC):

    path: str

    method: str

    vars: Dict

    args: Dict

    headers: RequestHeaders

    byte_data: input

    wsgi_input: WSGIInput

    def __init__(self, *, path: str, method: str, byte_data: bytes, headers: RequestHeaders):
        self.path = path
        self.method = method
        self.headers = headers
        self.wsgi_input = WSGIInput(
            byte_data=byte_data,
            headers=self.headers,
        )

    def get_arg(self, name: str) -> Union[str, int, bool]:
        """
        :param name:
        :type name:
        :return:
        :rtype:
        """
        arg_value = self.args[name]["value"]
        match self.args[name]["type"]:
            case "int":
                return int(arg_value)
            case "str":
                return arg_value
            case "bool":
                return bool(arg_value == "true" or arg_value == "True")

    def set_args(self, args):
        self.args = args

    def get_json(self) -> Dict:
        """

        :return:
        :rtype:
        """
        return self.wsgi_input.get_json()

    def get_body(self) -> str:
        """
        Handles text/plain
        :return:
        :rtype:
        """
        return self.wsgi_input.get_body()

    def get_form_data(self) -> Dict:
        """
        Handles application/x-www-form-urlencoded
        :return:
        :rtype:
        """
        return self.wsgi_input.get_form_data()

    def get_multipart_data(self) -> Dict:
        """
        Handles multipart/form-data
        :return:
        :rtype:
        """
        return self.wsgi_input.get_multipart_data()
