from abc import ABC, abstractmethod
from typing import Dict

from bobtail.wsgi_input import WSGIInput
from bobtail.exceptions import MultipartFormDataError, FormDataError


class AbstractForm(ABC):

    wsgi_input: WSGIInput

    def __init__(self, wsgi_input: WSGIInput):
        self.wsgi_input = wsgi_input

    @abstractmethod
    def get_field(self,field_name: str) -> str:
        pass


class Form(AbstractForm):

    def get_field(self,field_name: str) -> str:
        """
        :param field_name:
        :return str:
        """
        try:
            data = self.wsgi_input.get_form_data()
            return data[field_name]["value"]
        except KeyError as exc:
            raise FormDataError(
                f"Error getting form value for {field_name} field"
            ) from exc


class MultipartForm(AbstractForm):

    def get_field(self, field_name) -> str:
        """
        :param field_name:
        :return:
        """
        try:
            data = self.wsgi_input.get_multipart_data()
            return data[field_name]["value"]
        except KeyError as exc:
            raise MultipartFormDataError(
                f"Error getting form value for {field_name} field"
            ) from exc

    def get_file(self,field_name: str) -> Dict:
        """
        :param field_name:
        :return:
        """
        try:
            data = self.wsgi_input.get_multipart_data()
            return {
                "filename": data[field_name]["value"]["filename"],
                "data": data[field_name]["value"]["file_data"],
                "mimetype": data[field_name]["value"]["mimetype"],
            }
        except KeyError as exc:
            raise MultipartFormDataError(
                f"Error getting form value for {field_name} file"
            ) from exc

    def get_name(self,field_name: str) -> str:
        """
        :param field_name:
        :return:
        """
        try:
            data = self.wsgi_input.get_multipart_data()
            return data[field_name]["value"]["filename"]
        except KeyError as exc:
            raise MultipartFormDataError(
                f"Error getting filename for {field_name} file"
            ) from exc

    def get_data(self,field_name: str) -> bytes:
        """
        :param field_name:
        :return:
        """
        try:
            data = self.wsgi_input.get_multipart_data()
            return data[field_name]["value"]["file_data"]
        except KeyError as exc:
            raise MultipartFormDataError(
                f"Error getting file data for {field_name} file"
            ) from exc

    def get_mimetype(self,field_name: str) -> str:
        """
        :param field_name:
        :return:
        """
        try:
            data = self.wsgi_input.get_multipart_data()
            return data[field_name]["value"]["mimetype"]
        except KeyError as exc:
            raise MultipartFormDataError(
                f"Error getting file mimetype for {field_name} file"
            ) from exc
