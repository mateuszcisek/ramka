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
