from unittest.mock import Mock, patch

from web_framework.middleware import Middleware


@patch("web_framework.middleware.base_middleware.Request")
def test_call(mock_request):
    """
    When the middleware is called
    Then the request is created and the response is returned.
    """
    # pylint: disable=protected-access
    mock_handle_request = Mock()
    mock_app = Mock()
    mock_app.handle_request = mock_handle_request

    mock_environ = Mock()
    mock_start_response = Mock()

    middleware = Middleware(mock_app)
    response = middleware(mock_environ, mock_start_response)

    mock_request.assert_called_once_with(mock_environ)
    mock_handle_request.assert_called_once_with(mock_request.return_value)
    mock_handle_request.return_value.assert_called_once_with(
        mock_environ, mock_start_response
    )
    assert response == mock_handle_request.return_value.return_value


def test_handle_request():
    """
    When the handle_request method is called
    Then the request is handled and the response is returned
    And process_request method is called before the request is handled
    And process_response method is called after the request is handled.
    """
    # pylint: disable=protected-access
    mock_response = Mock()
    mock_handle_request = Mock(return_value=mock_response)
    mock_app = Mock(handle_request=mock_handle_request)

    mock_request = Mock()

    middleware = Middleware(mock_app)
    middleware.process_request = Mock()
    middleware.process_response = Mock()

    middleware.handle_request(mock_request)

    middleware.process_request.assert_called_once_with(mock_request)
    mock_handle_request.assert_called_once_with(mock_request)
    middleware.process_response.assert_called_once_with(mock_request, mock_response)


def test_add():
    """
    When the add method is called
    Then the middleware is added to the app
    """
    mock_app = Mock()
    mock_new_app = Mock()
    mock_middleware = Mock(return_value=mock_new_app)

    middleware = Middleware(mock_app)
    middleware.add(mock_middleware)

    mock_middleware.assert_called_once_with(mock_app)
    assert middleware._app == mock_new_app  # pylint: disable=protected-access
