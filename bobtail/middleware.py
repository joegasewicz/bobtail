from typing import List, Callable
from abc import ABC, abstractmethod

from bobtail.route import Handler
from bobtail.response import Response
from bobtail.request import Request

Tail = Callable[[Request, Response], None]


class AbstractMiddleware(ABC):

    @abstractmethod
    def run(self, req: Request, res: Response, tail: Tail) -> None:
        pass


class Middleware:

    middlewares: List[AbstractMiddleware] = None

    handler: Handler = None

    request: Request

    response: Response

    def add(self, instance: AbstractMiddleware):
        if self.middlewares is None:
            self.middlewares = []
        self.middlewares.append(instance)

    def call(self, req: Request, res: Response, handler: Handler):
        if self.middlewares:
            self.handler = handler
            self.request = req
            self.response = res
            for middleware in self.middlewares:
                middleware.run(self.request, self.response, self.tail)
            self.handler(self.request, self.response)
            return
        handler(req, res)

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
