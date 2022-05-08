from typing import Any, Callable, Dict, Optional, Union

from whitenoise import WhiteNoise

from web_framework.request import Request
from web_framework.response import Response
from web_framework.routing import BaseRouter, SimpleRouter
from web_framework.templates import BaseTemplateEngine, JinjaTemplateEngine
from web_framework.views import BaseView, default_error_handler, http_404


class App:
    def __init__(
        self,
        *,
        root_dir: str,
        static_dir: Optional[str] = None,
        router: Optional[BaseRouter] = None,
        router_kwargs: Optional[Dict] = None,
        template_engine: Optional[BaseTemplateEngine] = None,
        template_engine_kwargs: Optional[Dict] = None,
        http_404_not_found_handler: Optional[Callable] = None,
        error_handler: Optional[Callable] = None,
    ):
        self._router = router or SimpleRouter(**(router_kwargs or {}))
        self._template_engine = template_engine or JinjaTemplateEngine(
            **(template_engine_kwargs or {"root_dir": root_dir})
        )

        self._error_handler = error_handler or default_error_handler

        self._http_404_not_found_handler = http_404_not_found_handler

        self._whitenoise = WhiteNoise(self._wsgi_app, root=static_dir, prefix="static/")

    def __call__(self, environ, start_response):
        return self._whitenoise(environ, start_response)

    def _wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self._handle_request(request)
        return response(environ, start_response)

    def _handle_request(self, request: Request) -> Response:
        response = Response()
        parsed_route = self._router.resolve(request.path)

        try:
            if parsed_route:
                handler = parsed_route.get_handler(request.method)
                handler(request, response, **parsed_route.params)
            else:
                not_found_handler = self._http_404_not_found_handler or http_404
                not_found_handler(request, response)
        except Exception as error:
            if self._error_handler is None:
                raise error

            self._error_handler(request, response, error)

        return response

    def has_route(self, path: str) -> bool:
        return self._router.has_route(path)

    def add_route(self, path: str, view: Union[BaseView, Callable]) -> None:
        self._router.add_route(path, view)

    def route(self, path: str) -> Callable:
        return self._router.route(path)

    def template(self, template_name, context=None) -> Any:
        return self._template_engine.render(template_name, context)
