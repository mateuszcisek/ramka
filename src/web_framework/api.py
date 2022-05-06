from inspect import isclass

from parse import parse
from webob import Request, Response


class API:

    def __init__(self, force_trailing_slashes: bool = True):
        self.routes = {}
        self.force_trailing_slashes = force_trailing_slashes

    def _handle_trailing_slashes(self, path: str):
        if self.force_trailing_slashes and not path.endswith("/"):
            return f"{path}/"

        return path

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def find_handler(self, request_path):
        request_path = self._handle_trailing_slashes(request_path)

        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request_path=request.path)

        if handler is not None:
            if isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method not allowed", request.method)

            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def route(self, path):
        assert path not in self.routes, "Such route already exists."
        path = self._handle_trailing_slashes(path)

        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper
