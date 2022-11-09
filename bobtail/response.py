from typing import Dict, Tuple, List


class Response:
    status: int

    data: Dict

    headers: List[Tuple[str, str]]

    def __init__(self, data: Dict, status: int, headers: List[Tuple[str, str]]):
        self.data = data
        self.status = status
        self.headers = headers
