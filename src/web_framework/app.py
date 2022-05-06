from inspect import isclass
from typing import Callable, Dict, Tuple, Union

from parse import parse
from webob import Request, Response


class App:
    def __init__(self, force_trailing_slashes: bool = False):
        self._routes = {}
        self._force_trailing_slashes = force_trailing_slashes

    def __call__(self, environ: Dict, start_response: Callable) -> Response:
        request = Request(environ)
        response = self._handle_request(request)

        return response(environ, start_response)

    def _handle_trailing_slashes(self, path: str) -> str:
        if self._force_trailing_slashes and not path.endswith("/"):
            return f"{path}/"

        return path

    def _find_handler(
        self, request_path
    ) -> Tuple[Union[Callable, None], Union[str, None]]:
        request_path = self._handle_trailing_slashes(request_path)

        for path, handler in self._routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def _handle_request(self, request: Request) -> Response:
        response = Response()
        handler, kwargs = self._find_handler(request_path=request.path)

        if handler is not None:
            if isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method not allowed", request.method)

            handler(request, response, **kwargs)
        else:
            self._default_response(response)

        return response

    def _default_response(self, response: Response) -> None:
        response.status_code = 404
        response.text = "Not found."

    def has_route(self, path) -> bool:
        return path in self._routes

    def add_route(self, path: str, handler: Callable) -> None:
        assert not self.has_route(path), "Such route already exists."

        path = self._handle_trailing_slashes(path)
        self._routes[path] = handler

    def route(self, path: str) -> Callable:
        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper
