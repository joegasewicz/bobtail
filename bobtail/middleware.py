from typing import List, Callable
from abc import ABC, abstractmethod

from bobtail.route import Handler
from bobtail.response import Response
from bobtail.request import Request

Tail = Callable[[Request, Response], None]


class AbstractMiddleware(ABC):

    @abstractmethod
    def init(self, req: Request, res: Response, tail: Tail) -> None:
        pass


class Middleware:

    middlewares: List[AbstractMiddleware] = []

    handler: Handler = None

    request: Request

    response: Response

    def add(self, instance: AbstractMiddleware):
        self.middlewares.append(instance)

    def call(self, req: Request, res: Response, handler: Handler):
        self.handler = handler
        self.request = req
        self.response = res
        for middleware in self.middlewares:
            middleware.init(self.request, self.response, self.tail)
        self.handler(self.request, self.response)

    def tail(self, req: Request, res: Response) -> None:
        """
        :param req:
        :type req:
        :param res:
        :type res:
        :return:
        :rtype:
        """
        self.request = req
        self.response = res
        return
