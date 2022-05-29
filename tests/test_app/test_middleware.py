import tempfile
from unittest.mock import Mock, patch

from ramka.app import App


@patch("ramka.middleware.base_middleware.Request")
def test_middleware_call(mock_request):
    """
    When the application middleware is called
    Then the request is created and the response is returned.
    """
    # pylint: disable=protected-access
    mock_environ = {}
    mock_start_response = Mock()

    with tempfile.TemporaryDirectory() as root_dir:
        app = App(root_dir)
        app.handle_request = Mock()

        app._middleware(mock_environ, mock_start_response)

        mock_request.assert_called_once_with(mock_environ)
        app.handle_request.assert_called_once_with(mock_request.return_value)
        app.handle_request.return_value.assert_called_once_with(
            mock_environ, mock_start_response
        )
