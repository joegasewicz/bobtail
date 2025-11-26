from typing import Dict, Union
from abc import ABC
from warnings import warn

from bobtail.wsgi_input import WSGIInput
from bobtail.headers import RequestHeaders
from bobtail.exceptions import FormDataError, MultipartFormDataError
from bobtail.form import AbstractForm, Form, MultipartForm


class Request(ABC):

    path: str

    method: str

    vars: Dict

    args: Dict

    headers: RequestHeaders

    byte_data: bytes

    wsgi_input: WSGIInput

    form: Form

    query_str: str

    multipart: MultipartForm

    scheme: str

    domain: str

    _port: str

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        *,
        path: str,
        method: str,
        byte_data: bytes,
        headers: RequestHeaders,
        query_str: str,
        scheme: str,
        domain: str,
        port: str,
    ):
        self.path = path
        self.method = method
        self.headers = headers
        self.args: Dict = {}
        self.query_str = query_str
        self.wsgi_input = WSGIInput(
            byte_data=byte_data,
            headers=self.headers,
        )
        self.form = Form(self.wsgi_input)
        self.multipart = MultipartForm(self.wsgi_input)
        self.scheme = scheme
        self.domain = domain
        self._port = port

    @property
    def port(self) -> int:
        return int(self._port)

    @port.setter
    def port(self, value: str):
        self._port = value

    def get_path(self) -> str:
        """
        Get the full path from the incoming request. For example::

            def get(self, req, res):
                req_path = req.get_path()  # e.g. /articles/1

        :return: The full path represented as a string.
        """
        return self.path

    def get_arg(self, name: str) -> Union[str, int, bool, None]:
        """
        Get path argument values from incoming request.
        You can specify the type of Request arguments using curly braces & within the
        name & type seperated by a colon. For examples::

            /images/{id:int}/{name:str}/{is_raining:bool}

        To access request arguments inside a route handler, use the Request object's
        get_arg method, ror example::

            def get(self, req, res):
                id = req.get_args("id") # int
                name = req.get_args("name") # str
                is_raining = req.get_args("is_raining") # bool

        :param name: The name of the path variable.
        :return: The mapped path argument of the declared type.
        """
        if not self.args or name not in self.args:
            return None

        arg_value = self.args[name]["value"]
        arg_type = self.args[name]["type"]
        if arg_type == "int":
            return int(arg_value)
        if arg_type == "str":
            return arg_value
        if arg_type == "bool":
            return bool(arg_value == "true" or arg_value == "True")
        return None

    def set_args(self, args):
        self.args = args

    def get_json(self) -> Dict:
        """
        Get the
        :return:
        :rtype:
        """
        return self.wsgi_input.get_json()

    def get_body(self) -> str:
        """
        Gets the request body as a string. For example::

           def get(self, req, res):
                req_body = req.get_body()

        :return: Request body as a string.
        :rtype:
        """
        return self.wsgi_input.get_body()

    def get_form_data(self) -> Dict:
        """
        Handles application/x-www-form-urlencoded
        :return:
        :rtype:
        """
        warn(DeprecationWarning("[Bobtail]: Please use the Form API. See ..."))
        return self.wsgi_input.get_form_data()

    def get_multipart_data(self) -> Dict:
        """
        Handles multipart/form-data
        :return:
        :rtype:
        """
        warn(DeprecationWarning("[Bobtail]: Please use the MultipartForm API. See ..."))
        return self.wsgi_input.get_multipart_data()

    def get_form_value(self, name: str) -> str:
        """
        :param name:
        :return:
        """
        warn(DeprecationWarning("[Bobtail]: Please use the Form API. See ..."))
        try:
            data = self.get_form_data()
            return data[name]["value"]
        except KeyError as exc:
            raise FormDataError(
                f"Error getting form value for {name} field"
            ) from exc

    def get_multipart_value(self, name: str) -> str:
        """
        :param name:
        :return:
        """
        warn(DeprecationWarning("[Bobtail]: Please use the MultipartForm API. See ..."))
        try:
            data = self.get_multipart_data()
            return data[name]["value"]
        except KeyError as exc:
            raise MultipartFormDataError(
                f"Error getting form value for {name} field"
            ) from exc

    def get_filename_value(self, filename: str) -> str:
        """
        :param filename:
        :return:
        """
        warn(DeprecationWarning("[Bobtail]: Please use the MultipartForm API. See ..."))
        try:
            data = self.get_multipart_data()
            return data[filename]["value"]["filename"]
        except KeyError as exc:
            raise MultipartFormDataError(
                f"Filename Error: getting {filename} from multipart form data"
            ) from exc

    def get_params(self) -> Dict:
        """
        This method returns a dict of query params where the key
        is on the left side of the `=` sign & the value is 0n the right.
        For example::

            # for route "/images?name=joe&age=48"

            def get(self, req: Request, res: Response):
                result = req.get_params() # {"name": "joe", "age": "48"}

        :return: A dict that represents each set of query param.
        """
        param_dict = {}
        pl = self.query_str.split("&")
        for kv in pl:
            if "=" not in kv:
                continue
            k, v = kv.split("=")
            if not k:
                continue
            param_dict[k] = v
        return param_dict
