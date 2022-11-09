from typing import Dict


class Response:
    status: int

    data: Dict

    def __init__(self, data: Dict, status: int):
        self.data = data
        self.status = status
