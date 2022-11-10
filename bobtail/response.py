from typing import Dict, Tuple, List


class Response:

    _status: int = 200

    _data: Dict = None

    _headers: Dict = {
        "Content-Type": "application/json",
    }

    def __init__(self, data: Dict, status: int, headers: Dict):
        self._data = data
        self._status = status
        self._headers = headers

    @property
    def headers(self) -> Dict:
        return self._headers

    @headers.setter
    def headers(self, value: Dict):
        self._headers = {
            **self._headers,
            **value,
        }

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int):
        self._status = value

    def set_content_len(self) -> None:
        pass
