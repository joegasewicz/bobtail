from typing import List, Callable
from abc import ABC, abstractmethod

from bobtail.route import TypeRoute


class AbtractMiddleware(ABC):

    @abstractmethod
    def init(self) -> None:
        pass


class Middleware:

    routes: List[TypeRoute]

    def __init__(self, routes: List[TypeRoute]):
        self.routes = routes

    def add(self, instance: AbtractMiddleware):
        pass
