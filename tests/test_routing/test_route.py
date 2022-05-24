import pytest

from web_framework.routing import ResolvedRoute, Route


def test_get_handler_with_class_based_view(sample_class_view):
    """
    Given a class-based view
    When I get the handler for a HTTP method
    Then the handler should be the view's method.
    """
    route = Route("/sample_route", sample_class_view)
    handler = route.get_handler("GET")

    assert handler is not None
    assert handler.__name__ == "get"


def test_get_handler_with_class_based_view_incorrect_method(sample_class_view):
    """
    Given a class-based view
    When I get the handler for a HTTP method that does not exist
    Then a ValueError should be raised.
    """
    route = Route("/sample_route", sample_class_view)

    with pytest.raises(ValueError):
        route.get_handler("incorrect_view")


def test_get_handler_with_function_view(sample_func_view):
    """
    Given a function-based view
    When I get the handler for a HTTP method
    Then the handler should be the view.
    """
    route = Route("/sample_route", sample_func_view)
    handler = route.get_handler()

    assert handler is not None
    assert handler.__name__ == "sample_view"


def test_get_handler_with_function_view_incorrect_method(sample_func_view):
    """
    Given a function-based view
    When I get the handler for a HTTP method that does not exist
    Then a ValueError should be raised.
    """
    route = Route("/sample_route", sample_func_view)

    with pytest.raises(ValueError):
        route.get_handler("post")


def test_get_handler_with_incorrect_handler():
    """
    Given an incorrect route handler
    When I get the handler for the route
    Then an AttributeError should be raised.
    """
    route = Route("/sample_route", "incorrect_handler")

    with pytest.raises(AttributeError):
        route.get_handler("get")


def test_parsed_route_from_route(sample_class_view):
    """
    Given a route
    When I create a ParsedRoute from the route
    Then the ParsedRoute should have the same path and view as the route
    And the params should be correct
    """
    route = Route("/sample_route", sample_class_view)
    params = {"param": "value"}
    parsed_route = ResolvedRoute.from_route(route, params)

    assert parsed_route.path == route.path
    assert parsed_route.view == route.view
    assert parsed_route.params == params


def test_route_str_representation(sample_class_view):
    """
    When we fetch a string representation of a route
    Then we get a correct value as the result.
    """
    route = Route("/sample_route", sample_class_view)

    assert str(route) == f"/sample_route -> {str(sample_class_view)}"


def test_resolved_route_str_representation(sample_class_view):
    """
    When we fetch a string representation of a resolved route
    Then we get a correct value as the result.
    """
    route = Route("/sample_route", sample_class_view)
    resolved_route = ResolvedRoute.from_route(route, params={"a": "1", "b": "2"})

    assert str(resolved_route) == f"/sample_route ? a=1&b=2 -> {str(sample_class_view)}"
