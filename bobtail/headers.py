from abc import ABC


class BaseHeaders(ABC):

    content_type: str

    def __init__(self, content_type):
        self.content_type = content_type


class RequestHeaders(BaseHeaders):

    def __init__(self, content_type):
        super().__init__(content_type)

    def _get_type(self) -> str:
        return self.content_type.split(";")[0]

    def is_multipart(self) -> bool:
        """Is this a multipart-formdata request header"""
        if self._get_type() == "multipart/form-data":
            return True
        return False

    def is_urlencoded(self) -> bool:
        """Is this a application/x-www-form-urlencoded request header"""
        if self._get_type() == "application/x-www-form-urlencoded":
            return True
        return False


class ResponseHeaders(BaseHeaders):

    def __init__(self, content_type):
        super().__init__(content_type)
