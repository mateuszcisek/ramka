import pytest

from web_framework.routing import SimpleRouter


def test_simple_router_add_route(sample_func_view):
    """
    Given a router
    When I add a route using `add_route` method
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


def test_simple_router_route():
    """
    Given a router
    When I add a route using `route` decorator
    Then the router should have the route.
    And that route should have the correct path and view.
    """
    router = SimpleRouter()

    @router.route("/")
    def sample_view(_, response):
        response.text = "Hello, world!"

    assert len(router.routes) == 1

    route = router.routes[0]
    assert route.path == "/"
    assert route.view == sample_view  # pylint: disable=comparison-with-callable


def test_simple_router_resolve_with_non_existing_path(sample_func_view):
    """
    Given a router
    When I resolve a path that does not exist
    Then `None` should be returned.
    """
    router = SimpleRouter()
    router.add_route("/", sample_func_view)

    assert router.resolve("/another-view") is None


def test_simple_router_has_route(sample_func_view):
    """
    Given a router
    When I call `has_route` method
    Then a correct result is returned.
    """
    router = SimpleRouter()
    router.add_route("/", sample_func_view)

    assert router.has_route("/")
    assert not router.has_route("/another-view")


@pytest.mark.parametrize(
    "force_trailing_slashes,path,expected_result",
    (
        (True, "/sample/path", "/sample/path/"),
        (True, "/sample/path/", "/sample/path/"),
        (False, "/sample/path", "/sample/path"),
        (False, "/sample/path/", "/sample/path/"),
    ),
)
def test_simple_router_handle_trailing_slashes(
    force_trailing_slashes, path, expected_result
):
    """
    Given a router with `force_trailing_slashes` set
    When I process a path with `_handle_trailing_slashes` method
    Then I get a correct result.
    """
    router = SimpleRouter(force_trailing_slashes=force_trailing_slashes)

    # pylint: disable=protected-access
    assert router._handle_trailing_slashes(path) == expected_result
