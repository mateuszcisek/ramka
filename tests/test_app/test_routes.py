import pytest


def test_new_route(create_app):
    app = create_app()

    @app.route("/example_route")
    def _(req, resp):
        resp.text = "Sample response"

    assert app.has_route("/example_route")
    assert not app.has_route("/example_route/")


def test_new_route_with_trailing_slashed_forced(create_app):
    app = create_app(force_trailing_slashes=True)

    @app.route("/example_route")
    def example_route(req, resp):
        resp.text = "Sample response"

    assert not app.has_route("/example_route")
    assert app.has_route("/example_route/")


def test_new_route_with_existing_path(create_app):
    app = create_app()

    @app.route("/example_route")
    def example_route(req, resp):
        resp.text = "Sample response"

    with pytest.raises(AssertionError):
        @app.route("/example_route")
        def example_route_2(req, resp):
            resp.text = "Another response"
