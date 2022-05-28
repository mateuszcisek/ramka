import tempfile
from unittest.mock import Mock, patch

from ramka.app import App


@patch("ramka.app.Request")
def test_wsgi_app_call(mock_request):
    """
    When the WSGI application is called
    Then the request is created and the response is returned.
    """
    # pylint: disable=protected-access
    mock_environ = Mock()
    mock_start_response = Mock()

    with tempfile.TemporaryDirectory() as root_dir:
        app = App(root_dir)
        app._handle_request = Mock()

        app._wsgi_app(mock_environ, mock_start_response)

        mock_request.assert_called_once_with(mock_environ)
        app._handle_request.assert_called_once_with(mock_request.return_value)
        app._handle_request.return_value.assert_called_once_with(
            mock_environ, mock_start_response
        )
