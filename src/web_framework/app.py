from typing import Any, Callable, Dict, List, Optional, Type, Union

from whitenoise import WhiteNoise

from web_framework.middleware import Middleware
from web_framework.request import Request
from web_framework.response import Response
from web_framework.routing import BaseRouter, SimpleRouter
from web_framework.templates import BaseTemplateEngine, JinjaTemplateEngine
from web_framework.views import (
    BaseView,
    default_error_handler,
    http_404_not_found,
    http_405_method_not_allowed,
)


class App:
    """The main application class.

    This is the entrypoint for the application.
    """

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
        http_405_not_found_handler: Optional[Callable] = None,
        error_handler: Optional[Callable] = None,
        middleware_classes: Optional[List[Type[Middleware]]] = None,
    ):
        """Initialize the application.

        Arguments:
            root_dir (str): The root directory of the application.
            static_dir (Optional[str]): The directory containing static files.
            router (Optional[BaseRouter]): The router to use.
            router_kwargs (Optional[Dict]): The kwargs to pass to the router.
            template_engine (Optional[BaseTemplateEngine]): The template engine to use.
            template_engine_kwargs (Optional[Dict]): The kwargs to pass to the template
                engine.
            http_404_not_found_handler (Optional[Callable]): The handler to use for
                HTTP 404 error.
            error_handler (Optional[Callable]): The handler to use for errors.
            middleware_classes (Optional[List[Type[Middleware]]]): The list of
                middleware classes to use.

        """
        self._router = router or SimpleRouter(**(router_kwargs or {}))
        self._template_engine = template_engine or JinjaTemplateEngine(
            **(template_engine_kwargs or {"root_dir": root_dir})
        )

        self._error_handler = error_handler or default_error_handler

        self._http_404_not_found_handler = http_404_not_found_handler
        self._http_405_not_found_handler = http_405_not_found_handler

        self._whitenoise = WhiteNoise(self._wsgi_app, root=static_dir, prefix="static/")

        self._middleware = Middleware(self)
        if middleware_classes:
            for middleware_class in middleware_classes:
                self._middleware.add(middleware_class)

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
                handler = self._http_404_not_found_handler or http_404_not_found
                handler(request, response)

        except NotImplementedError:
            handler = self._http_405_not_found_handler or http_405_method_not_allowed
            handler(request, response)

        # Using `Exception` class as we want to catch all exception here.
        except Exception as error:  # pylint: disable=broad-except
            if self._error_handler is None:
                raise error

            self._error_handler(request, response, error)

        return response

    def has_route(self, path: str) -> bool:
        """Check if the router has a route for the given path.

        Arguments:
            path (str): The path to check.

        Returns:
            (bool): True if the router has a route for the given path, False otherwise.
        """
        return self._router.has_route(path)

    def add_route(
        self,
        path: str,
        view: Union[BaseView, Callable],
        methods: Optional[List[str]] = None,
    ) -> None:
        """Add a route to the router.

        It's supposed to be used as a method.

        Arguments:
            path (str): The path to add the route to.
            view (Union[BaseView, Callable]): The view to add the route to.
            methods (Optional[List[str]]): The list of methods to add the route to.
        """
        self._router.add_route(path, view, methods)

    def route(self, path: str, methods: Optional[List[str]] = None) -> Callable:
        """Add a route to the router.

        It's supposed to be used as a decorator.

        Arguments:
            path (str): The path to add the route to.
            methods (Optional[List[str]]): The list of methods to add the route to.
        """
        return self._router.route(path, methods)

    def template(self, template_name, context: Dict[str, Any] = None) -> Any:
        """Render a template using defined template engine.

        Arguments:
            template_name (str): The name of the template to render.
            context (Optional[Dict[str, Any]]): The context to use.

        Returns:
            (Any): The rendered template.
        """
        return self._template_engine.render(template_name, context)
