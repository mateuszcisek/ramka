import tempfile
from unittest.mock import Mock

from ramka.app import App


def test_app_call_with_static_files_engine():
    """
    When the app is initialized with a static files engine
    And the app is called
    Then the `_static_files_engine` method is called
    And the `_middleware` method is not called.
    """
    # pylint: disable=protected-access

    environ_mock = Mock()
    start_response_mock = Mock()

    with tempfile.TemporaryDirectory() as root_dir:
        mock_static_files_engine = Mock()
        app = App(
            root_dir,
            static_files_dir=root_dir,
            static_files_engine=mock_static_files_engine,
        )
        app._middleware = Mock()
        app(environ_mock, start_response_mock)

        app._static_files_engine.assert_called_once_with(
            environ_mock, start_response_mock
        )


def test_app_call_without_static_files_engine():
    """
    When the app is initialized without a static files engine
    And the app is called
    Then the `_middleware` method is called
    And the `_static_files_engine` method is not set.
    """
    # pylint: disable=protected-access

    environ_mock = Mock()
    start_response_mock = Mock()

    with tempfile.TemporaryDirectory() as root_dir:
        app = App(root_dir)
        app._middleware = Mock()
        app(environ_mock, start_response_mock)

        assert not app._static_files_engine
        app._middleware.assert_called_once_with(environ_mock, start_response_mock)
