from typing import Dict, Union


class Request:

    path: str

    method: str

    vars: Dict

    args: Dict

    def __init__(self, path: str, method: str):
        self.path = path
        self.method = method

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
