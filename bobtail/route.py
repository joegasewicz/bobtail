from abc import ABC, abstractmethod
from typing import List, Tuple

from bobtail.response import Response
from bobtail.request import Request


class AbstractRoute(ABC):

    @abstractmethod
    def get(self, req: Request, res: Response) -> None:
        """
        :param req:
        :type req:
        :param res:
        :type res:
        :return:
        :rtype:
        """

    @abstractmethod
    def post(self, req: Request, res: Response) -> None:
        """
        :param req:
        :type req:
        :param res:
        :type res:
        :return:
        :rtype:
        """

    @abstractmethod
    def put(self, req: Request, res: Response) -> None:
        """
        :param req:
        :type req:
        :param res:
        :type res:
        :return:
        :rtype:
        """

    @abstractmethod
    def delete(self, req: Request, res: Response) -> None:
        """
        :param req:
        :type req:
        :param res:
        :type res:
        :return:
        :rtype:
        """


TypeRoute = Tuple[AbstractRoute, str]
