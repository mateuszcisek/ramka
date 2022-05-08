import pytest
from web_framework.routing import Route, SimpleRouteResolver


def test_simple_route_resolver_add_route(sample_func_view):
    resolver = SimpleRouteResolver()

    assert not resolver._routes

    resolver.add_route("/", sample_func_view)

    assert len(resolver._routes) == 1

    route = resolver._routes[0]
    assert route.path == "/"
    assert route.view == sample_func_view


def test_simple_route_resolver_add_route_with_existing_path(sample_func_view):
    resolver = SimpleRouteResolver()
    resolver.add_route("/", sample_func_view)

    with pytest.raises(AttributeError):
        resolver.add_route("/", sample_func_view)

