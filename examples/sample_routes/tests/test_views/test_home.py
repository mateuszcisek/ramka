import pytest

from examples.sample_routes.app import app


def test_home(create_session):
    """
    Given the app,
    When the user visits the home page,
    Then a correct response is returned.
    """
    session = create_session(app)
    response = session.get("/")

    assert response.status_code == 200
    assert "<title>Sample template view</title>" in response.text
    assert "This is a sample template." in response.text


def test_text(create_session):
    """
    Given the app,
    When the user visits the text page,
    Then a correct response is returned.
    """
    session = create_session(app)
    response = session.get("/text/")

    assert response.status_code == 200
    assert response.text == "Hello!"


def test_external(create_session):
    """
    Given the app,
    When the user visits the text page,
    Then a correct response is returned.
    """
    session = create_session(app)
    response = session.get("/external/")

    assert response.status_code == 200
    assert response.text == "External route"


def test_hello(create_session):
    """
    Given the app,
    When the user visits the hello page with a name,
    Then a correct response is returned.
    """
    session = create_session(app)
    response = session.get("/hello/sample-name/")

    assert response.status_code == 200
    assert response.text == "Hello sample-name!"


def test_add(create_session):
    """
    Given the app,
    When the user visits the add page with a two numbers,
    Then a correct response is returned.
    """
    session = create_session(app)
    response = session.get("/add/3/4/")

    assert response.status_code == 200
    assert response.text == "Sum: 7"


@pytest.mark.parametrize(
    "method,expected_status_code,expected_text",
    (
        ("get", 200, "HTTP method: GET!"),
        ("post", 200, "HTTP method: POST!"),
        ("put", 405, '{"error": "Method not allowed."}'),
        ("delete", 405, '{"error": "Method not allowed."}'),
        ("patch", 405, '{"error": "Method not allowed."}'),
    ),
)
def test_limited_view(create_session, method, expected_status_code, expected_text):
    """
    Given the app with a function-based view with limited available methods,
    When I visit the view using the specified method
    Then a correct response is returned.
    """
    session = create_session(app)
    response = getattr(session, method)("/limited-view/")

    assert response.status_code == expected_status_code
    assert response.text == expected_text


@pytest.mark.parametrize(
    "method,expected_status_code,expected_text",
    (
        ("get", 200, "Sample class-view GET page"),
        ("post", 200, "Sample class-view POST page"),
        ("put", 405, '{"error": "Method not allowed."}'),
        ("delete", 405, '{"error": "Method not allowed."}'),
        ("patch", 405, '{"error": "Method not allowed."}'),
    ),
)
def test_class_based_view_get(
    create_session, method, expected_status_code, expected_text
):
    """
    Given the app with a class-based view with limited available methods,
    When I visit the view using the specified method
    Then a correct response is returned.
    """
    session = create_session(app)
    response = getattr(session, method)("/class-view/")

    assert response.status_code == expected_status_code
    assert response.text == expected_text
