import tempfile
from unittest.mock import Mock, patch

import pytest

from ramka.app import App


@patch("ramka.app.Response")
def test_handle_request_success(mock_response_cls):
    """
    When the method `_handle_request` is called
    And the request path is valid
    And the request method is valid
    Then the response should be returned
    And the error handlers are not called.
    """
    # pylint: disable=protected-access
    with tempfile.TemporaryDirectory() as root_dir:
        mock_parsed_route = Mock()
        mock_parsed_route.params = {"foo": "bar"}

        mock_router = Mock()
        mock_router.resolve.return_value = mock_parsed_route

        mock_response = Mock()
        mock_response_cls.return_value = mock_response

        mock_request = Mock()
        mock_404_handler = Mock()
        mock_405_handler = Mock()
        mock_error_handler = Mock()

        app = App(
            root_dir,
            router=mock_router,
            http_404_not_found_handler=mock_404_handler,
            http_405_method_not_allowed_handler=mock_405_handler,
            error_handler=mock_error_handler,
        )

        result = app.handle_request(mock_request)

        mock_router.resolve.assert_called_once_with(mock_request.path)
        mock_parsed_route.get_handler.assert_called_once_with(mock_request.method)
        mock_parsed_route.get_handler.return_value.assert_called_once_with(
            mock_request, mock_response, foo="bar"
        )
        mock_404_handler.assert_not_called()
        mock_405_handler.assert_not_called()
        mock_error_handler.assert_not_called()
        assert result == mock_response


@patch("ramka.app.Response")
def test_handle_request_invalid_path(mock_response_cls):
    """
    When the method `_handle_request` is called
    And the request path is invalid
    Then the error should be handled with a valid method.
    """
    # pylint: disable=protected-access
    with tempfile.TemporaryDirectory() as root_dir:
        mock_router = Mock()
        mock_router.resolve.return_value = None

        mock_response = Mock()
        mock_response_cls.return_value = mock_response

        mock_request = Mock()
        mock_404_handler = Mock()
        mock_405_handler = Mock()
        mock_error_handler = Mock()

        app = App(
            root_dir,
            router=mock_router,
            http_404_not_found_handler=mock_404_handler,
            http_405_method_not_allowed_handler=mock_405_handler,
            error_handler=mock_error_handler,
        )

        result = app.handle_request(mock_request)

        mock_router.resolve.assert_called_once_with(mock_request.path)
        mock_404_handler.assert_called_once_with(mock_request, mock_response)
        mock_405_handler.assert_not_called()
        mock_error_handler.assert_not_called()
        assert result == mock_response


@patch("ramka.app.Response")
def test_handle_request_handler_not_implemented(mock_response_cls):
    """
    When the method `_handle_request` is called
    And route handler is not implemented
    Then the error should be handled with a valid method.
    """
    # pylint: disable=protected-access
    with tempfile.TemporaryDirectory() as root_dir:
        mock_parsed_route = Mock()
        mock_parsed_route.get_handler.side_effect = NotImplementedError

        mock_router = Mock()
        mock_router.resolve.return_value = mock_parsed_route

        mock_response = Mock()
        mock_response_cls.return_value = mock_response

        mock_request = Mock()
        mock_404_handler = Mock()
        mock_405_handler = Mock()
        mock_error_handler = Mock()

        app = App(
            root_dir,
            router=mock_router,
            http_404_not_found_handler=mock_404_handler,
            http_405_method_not_allowed_handler=mock_405_handler,
            error_handler=mock_error_handler,
        )

        result = app.handle_request(mock_request)

        mock_router.resolve.assert_called_once_with(mock_request.path)
        mock_405_handler.assert_called_once_with(mock_request, mock_response)
        mock_404_handler.assert_not_called()
        mock_error_handler.assert_not_called()
        assert result == mock_response


@patch("ramka.app.Response")
def test_handle_request_handler_raised_error(mock_response_cls):
    """
    When the method `_handle_request` is called
    And route handler raises an unexpected error
    Then the error should be handled with a valid method.
    """
    # pylint: disable=protected-access
    with tempfile.TemporaryDirectory() as root_dir:
        mock_parsed_route = Mock()
        mock_parsed_route.get_handler.side_effect = ValueError

        mock_router = Mock()
        mock_router.resolve.return_value = mock_parsed_route

        mock_response = Mock()
        mock_response_cls.return_value = mock_response

        mock_request = Mock()
        mock_404_handler = Mock()
        mock_405_handler = Mock()
        mock_error_handler = Mock()

        app = App(
            root_dir,
            router=mock_router,
            http_404_not_found_handler=mock_404_handler,
            http_405_method_not_allowed_handler=mock_405_handler,
            error_handler=mock_error_handler,
        )

        result = app.handle_request(mock_request)

        mock_router.resolve.assert_called_once_with(mock_request.path)

        error_handler_first_call_args = mock_error_handler.call_args_list[0].args
        assert error_handler_first_call_args[0] == mock_request
        assert error_handler_first_call_args[1] == mock_response
        assert isinstance(error_handler_first_call_args[2], ValueError)

        mock_405_handler.assert_not_called()
        mock_404_handler.assert_not_called()
        assert result == mock_response


def test_handle_request_handler_raised_error_with_no_error_handler():
    """
    When the method `handle_request` is called
    And route handler raises an unexpected error
    And the error handler is not defined in the app
    Then the error is raised.
    """
    # pylint: disable=protected-access
    with tempfile.TemporaryDirectory() as root_dir:
        mock_parsed_route = Mock()
        mock_parsed_route.get_handler.side_effect = ValueError

        mock_router = Mock()
        mock_router.resolve.return_value = mock_parsed_route

        mock_request = Mock()

        app = App(root_dir, router=mock_router)
        app._error_handler = None

        with pytest.raises(ValueError):
            app.handle_request(mock_request)
