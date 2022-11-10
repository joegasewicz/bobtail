from typing import Dict


class Request:

    path: str

    method: str

    vars: Dict

    def __init__(self, path: str, method: str):
        self.path = path
        self.method = method
