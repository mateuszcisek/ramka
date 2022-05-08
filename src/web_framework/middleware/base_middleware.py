from typing import Type

from web_framework.request import Request
from web_framework.response import Response


class BaseMiddleware:
    def __init__(self, app):
        self._app = app

    def __call__(self, environ, start_response) -> Response:
        request = Request(environ)
        response = self.app.handle_request(request)

        return response(environ, start_response)

    def add(self, middleware_cls: Type["BaseMiddleware"]):
        self._app = middleware_cls(self._app)

    def handle_request(self, request: Request) -> Response:
        self.process_request(request)
        response = self._app.handle_request(request)
        self.process_response(request, response)

        return response

    def process_request(self, request: Request) -> None:
        pass

    def process_response(self, request: Request, response: Response) -> None:
        pass
