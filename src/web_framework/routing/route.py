from inspect import isclass
from typing import Any, Callable, Dict, List, Optional, Union

from web_framework.views import BaseView


class Route:
    """Route representation.

    A single route defines a path (e.g. `/users/`) and a view (e.g. UserView).

    The path should always be absolute which means it should start with a forward slash.
    It can consist of multiple arguments (e.g. `/users/{id}/`) and needs to be unique.

    The view can be either a class (that inherits from `web_framework.views.BaseView`)
    or a function that accepts two arguments: the request and the response. For
    function-based views, additional argument with all supported methods can be
    specified. By default, each view only supports GET requests. For class-based views,
    the view can have multiple methods (e.g. get, post, put, delete, etc.) and the
    handler will be selected based on the request method.

    Each argument can have a type specified. For example, path `/users/{id:d}/` means
    that the argument `id` should be a decimal number. For full list of supported types
    see https://github.com/r1chardj0n3s/parse#format-specification.
    """

    def __init__(
        self,
        path: str,
        view: Union[BaseView, Callable],
        methods: Optional[List[str]] = None,
    ):
        self.path = path
        self.view = view
        self.methods = methods or ["GET"]

    def get_handler(self, method: Optional[str] = "GET") -> Callable:
        if isclass(self.view):
            if not method:
                raise ValueError("Method is required for class-based views.")

            handler = getattr(self.view(), method.lower(), None)
            if handler is None:
                raise AttributeError(f"Method {method} is not allowed.")

            return handler

        if method not in self.methods:
            raise ValueError(f"Method {method} is not allowed.")

        return self.view

    def __str__(self) -> str:
        return f"{self.path} -> {self.view}"

    def __repr__(self) -> str:
        return f"{self.path} -> {self.view}"


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
        return f"{self.path} ? {self.params} -> {self.view}"

    def __repr__(self) -> str:
        return f"{self.path} ? {self.params} -> {self.view}"


__all__ = ["Route", "ParsedRoute"]
