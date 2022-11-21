from enum import Enum
from typing import Union, Dict, Optional
import json
from birman import Decoder

from bobtail.headers import RequestHeaders


class WSGIInput:

    byte_data: bytes

    headers: RequestHeaders

    def __init__(self, byte_data: bytes, headers: RequestHeaders):
        self.byte_data = byte_data
        self.headers = headers

    def get_json(self) -> Dict:
        if self.headers.content_type == "application/json":
            if self.byte_data:
                return json.loads(self.byte_data)
        return {}

    def get_form_data(self) -> Dict:
        if self.byte_data and self.headers.is_urlencoded():
            d = Decoder(self.byte_data)
            form_dict = d.decode()
            return form_dict
        return {}

    def get_multipart_data(self) -> Dict:
        if self.byte_data and self.headers.is_multipart():
            d = Decoder(self.byte_data)
            form_dict = d.decode()
            return form_dict
        return {}

    def get_body(self) -> str:
        return str(self.byte_data, "utf-8")
