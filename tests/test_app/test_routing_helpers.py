import tempfile
from unittest.mock import Mock

from ramka.app import App


def test_add_route_calls_router_method():
    """
    When the method `add_route` is called on App object
    Then the method `add_route` should be called with the correct arguments
        on the router.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        mock_router = Mock()
        mock_handler = Mock()

        app = App(root_dir, router=mock_router)

        app.add_route("/sample_route", mock_handler, ["GET", "POST"])

        mock_router.add_route.assert_called_once_with(
            "/sample_route", mock_handler, ["GET", "POST"]
        )


def test_route_calls_router_method():
    """
    When the method `route` is called on App object
    Then the method `route` should be called with the correct arguments on the router.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        mock_router = Mock()

        app = App(root_dir, router=mock_router)

        app.route("/sample_route", ["GET", "POST"])

        mock_router.route.assert_called_once_with("/sample_route", ["GET", "POST"])


def test_has_route_calls_router_method():
    """
    When the method `has_route` is called on App object
    Then the method `has_route` should be called with the correct arguments
        on the router.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        mock_router = Mock()

        app = App(root_dir, router=mock_router)

        app.has_route("/sample_route")

        mock_router.has_route.assert_called_once_with("/sample_route")
