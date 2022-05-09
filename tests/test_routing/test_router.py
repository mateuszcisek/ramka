import pytest

from web_framework.routing import SimpleRouter


def test_simple_router_add_route(sample_func_view):
    """
    Given a router
    When I add a route
    Then the router should have the route.
    And that route should have the correct path and view.
    """
    router = SimpleRouter()

    assert not router.routes

    router.add_route("/", sample_func_view)

    assert len(router.routes) == 1

    route = router.routes[0]
    assert route.path == "/"
    assert route.view == sample_func_view


def test_simple_router_add_route_with_existing_path(sample_func_view):
    """
    Given a router with a route
    When I add a route with the same path
    Then an AttributeError should be raised.
    """
    router = SimpleRouter()
    router.add_route("/", sample_func_view)

    with pytest.raises(AttributeError):
        router.add_route("/", sample_func_view)
