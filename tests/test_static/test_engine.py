import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from web_framework.static.engine import WhiteNoiseEngine


def test_whitenoise_engine_initialized_with_correct_files():
    """
    Given two directories with static files and a WhiteNoiseEngine
    When I initialize the engine
    Then all static files should be registered by the engine.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        # Given
        dir_1_path = os.path.join(root_dir, "module_1")
        dir_2_path = os.path.join(root_dir, "module_2")

        os.makedirs(dir_1_path)
        os.makedirs(dir_2_path)

        Path(os.path.join(dir_1_path, "file_1.css")).touch()
        Path(os.path.join(dir_2_path, "file_2.jpg")).touch()

        # When
        engine = WhiteNoiseEngine(Mock(), root_dir)

        # Then
        assert engine.has_file("/static/module_1/file_1.css")
        assert engine.has_file("/static/module_2/file_2.jpg")


@patch("web_framework.static.engine.os.path.isdir")
def test_whitenoise_engine_call_calls_correct_methods(mock_isdir):
    """
    Given a WhiteNoiseEngine
    When I call the engine
    Then the WhiteNoise object should be called with the correct arguments.
    """
    # pylint: disable=no-member, protected-access
    with tempfile.TemporaryDirectory() as root_dir:
        mock_isdir.return_value = True

        mock_environ = Mock()
        mock_start_response = Mock()

        engine = WhiteNoiseEngine(Mock(), root_dir)
        engine._env = Mock()
        engine(mock_environ, mock_start_response)

        engine._env.assert_called_once_with(mock_environ, mock_start_response)
