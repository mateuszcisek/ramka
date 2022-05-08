import pytest

from web_framework.routing import Route, SimpleRouter


def test_simple_router_add_route(sample_func_view):
    router = SimpleRouter()

    assert not router._routes

    router.add_route("/", sample_func_view)

    assert len(router._routes) == 1

    route = router._routes[0]
    assert route.path == "/"
    assert route.view == sample_func_view


def test_simple_router_add_route_with_existing_path(sample_func_view):
    router = SimpleRouter()
    router.add_route("/", sample_func_view)

    with pytest.raises(AttributeError):
        router.add_route("/", sample_func_view)
