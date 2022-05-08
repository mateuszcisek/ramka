from abc import ABC, abstractmethod
from typing import Callable, List, Union

from parse import parse

from web_framework.routing.route import ParsedRoute, Route
from web_framework.views import BaseView


class BaseRouter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def add_route(self, path: str, view: Union[BaseView, Callable]) -> None:
        pass

    @abstractmethod
    def route(self, path: str) -> Callable:
        pass

    @abstractmethod
    def resolve(self, path: str = None) -> Route:
        pass


class SimpleRouter:
    def __init__(self, force_trailing_slashes: bool = True):
        super().__init__()

        self._routes: List[Route] = []
        self._force_trailing_slashes = force_trailing_slashes

    def _handle_trailing_slashes(self, path: str) -> str:
        if self._force_trailing_slashes and not path.endswith("/"):
            return f"{path}/"

        return path

    def resolve(self, path: str) -> ParsedRoute:
        path = self._handle_trailing_slashes(path)
        for route in self._routes:
            parsed_path = parse(route.path, path)
            if parsed_path:
                return ParsedRoute(route.path, route.view, parsed_path.named)

        return None

    def has_route(self, path: str) -> bool:
        return self.resolve(path) is not None

    def add_route(self, path: str, view: Union[BaseView, Callable]) -> None:
        if self.has_route(path):
            raise AttributeError("Route already exists.")

        self._routes.append(Route(self._handle_trailing_slashes(path), view))

    def route(self, path: str) -> Callable:
        def wrapper(view: Union[BaseView, Callable]):
            self.add_route(path, view)
            return view

        return wrapper


__all__ = ["BaseRouter", "SimpleRouter"]
