import pytest

from web_framework.routing import SimpleRouter


def test_simple_router_add_route(sample_func_view):
    router = SimpleRouter()

    assert not router.routes

    router.add_route("/", sample_func_view)

    assert len(router.routes) == 1

    route = router.routes[0]
    assert route.path == "/"
    assert route.view == sample_func_view


def test_simple_router_add_route_with_existing_path(sample_func_view):
    router = SimpleRouter()
    router.add_route("/", sample_func_view)

    with pytest.raises(AttributeError):
        router.add_route("/", sample_func_view)
