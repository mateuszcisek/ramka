import pytest

from web_framework.routing import ResolvedRoute, Route


def test_get_handler_with_class_based_view(sample_class_view):

    route = Route("/sample_route", sample_class_view)
    handler = route.get_handler("GET")

    assert handler is not None
    assert handler.__name__ == "get"


def test_get_handler_with_class_based_view_and_incorrect_method_name(sample_class_view):
    route = Route("/sample_route", sample_class_view)

    with pytest.raises(AttributeError):
        route.get_handler("POST")


def test_get_handler_with_function_view(sample_func_view):

    route = Route("/sample_route", sample_func_view)
    handler = route.get_handler()

    assert handler is not None
    assert handler.__name__ == "sample_view"


def test_parsed_route_from_route(sample_class_view):

    route = Route("/sample_route", sample_class_view)
    params = {"param": "value"}
    parsed_route = ResolvedRoute.from_route(route, params)

    assert parsed_route.path == route.path
    assert parsed_route.view == route.view
    assert parsed_route.params == params
