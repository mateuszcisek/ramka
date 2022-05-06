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


def test_route_response_is_correct(create_app, create_session):
    app = create_app()
    session = create_session(app)

    response_test = "Sample response"

    @app.route("/sample_endpoint")
    def sample_endpoint(req, resp):
        resp.text = response_test

    response = session.get("/sample_endpoint")

    assert response.text == response_test
    assert response.status_code == 200


def test_parameterized_route_response_is_correct(create_app, create_session):
    app = create_app()
    session = create_session(app)

    @app.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    response = session.get("/john")

    assert response.text == "hey john"
    assert response.status_code == 200


def test_default_404_response(create_app, create_session):
    app = create_app()
    session = create_session(app)

    response = session.get("/doesnotexist")

    assert response.status_code == 404
    assert response.text == "Not found."


def test_class_based_handler_get(create_app, create_session):
    app = create_app()
    session = create_session(app)

    response_text = "Sample response"

    @app.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = response_text

    response = session.get("/book")

    assert response.text == response_text
    assert response.status_code == 200


def test_class_based_handler_post(create_app, create_session):
    app = create_app()
    session = create_session(app)

    response_text = "Sample response"

    @app.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text

    response = session.post("/book")

    assert response.text == response_text
    assert response.status_code == 200


def test_class_based_handler_not_allowed_method(create_app, create_session):
    app = create_app()
    session = create_session(app)

    @app.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = "Sample response"

    with pytest.raises(AttributeError):
        session.get("/book")
