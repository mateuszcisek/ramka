import os
from typing import Callable, Union

from jinja2 import Environment, FileSystemLoader, Template
from webob import Request, Response
from whitenoise import WhiteNoise

from web_framework.routing import BaseRouteResolver, SimpleRouteResolver
from web_framework.views.base_view import BaseView
from web_framework.views.errors import http_404


class App:
    def __init__(
        self,
        *,
        templates_dir: str = None,
        static_dir: str = None,
        route_resolver: BaseRouteResolver = None,
        http_404_not_found_handler: Callable = None,
    ):
        self._route_resolver = route_resolver or SimpleRouteResolver()
        self._http_404_not_found_handler = http_404_not_found_handler

        self._templates_env = (
            Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))
            if templates_dir
            else None
        )

        self._whitenoise = WhiteNoise(self._wsgi_app, root=static_dir, prefix="static/")

    def __call__(self, environ, start_response):
        return self._whitenoise(environ, start_response)

    def _wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self._handle_request(request)
        return response(environ, start_response)

    def _handle_request(self, request: Request) -> Response:
        response = Response()
        parsed_route = self._route_resolver.resolve(request.path)

        if parsed_route:
            handler = parsed_route.get_handler(request.method)
            handler(request, response, **parsed_route.params)
        else:
            not_found_handler = self._http_404_not_found_handler or http_404
            not_found_handler(request, response)

        return response

    def has_route(self, path: str) -> bool:
        return self._route_resolver.has_route(path)

    def add_route(self, path: str, view: Union[BaseView, Callable]) -> None:
        self._route_resolver.add_route(path, view)

    def route(self, path: str) -> Callable:
        return self._route_resolver.route(path)

    def template(self, template_name, context=None) -> Template:
        if not self._templates_env:
            raise RuntimeError("Templates directory is not set.")

        if context is None:
            context = {}

        return self._templates_env.get_template(template_name).render(**context)
