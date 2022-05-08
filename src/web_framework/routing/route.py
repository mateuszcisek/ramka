from inspect import isclass
from typing import Any, Callable, Dict, Optional, Union

from web_framework.views import BaseView


class Route:
    def __init__(self, path: str, view: Union[BaseView, Callable]):
        self.path = path
        self.view = view

    def get_handler(self, method: Optional[str] = None) -> Callable:
        if isclass(self.view):
            if not method:
                raise ValueError("Method is required for class-based views.")

            handler = getattr(self.view(), method.lower(), None)
            if handler is None:
                raise AttributeError("Method not allowed: %s" % method)

            return handler

        if method:
            raise ValueError("Method is not allowed for function-based views.")

        return self.view

    def __str__(self) -> str:
        return "%s -> %s" % (self.path, self.view)

    def __repr__(self) -> str:
        return "%s -> %s" % (self.path, self.view)


class ParsedRoute(Route):
    def __init__(
        self, path: str, view: Union[BaseView, Callable], params: Dict[str, Any]
    ):
        super().__init__(path, view)
        self.params = params

    @staticmethod
    def from_route(route: Route, params: Dict) -> "ParsedRoute":
        return ParsedRoute(route.path, route.view, params)

    def __str__(self) -> str:
        return "%s ? %s -> %s" % (self.path, self.params, self.view)

    def __repr__(self) -> str:
        return "%s ? %s -> %s" % (self.path, self.params, self.view)


__all__ = ["Route", "ParsedRoute"]
