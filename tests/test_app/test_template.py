import tempfile
from unittest.mock import Mock

from web_framework.app import App


def test_template_calls_router_method():
    """
    When the method `template` is called on App object
    Then the method `render` should be called with the correct arguments
        on the template engine.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        mock_template_engine = Mock()
        mock_context = {"foo": "bar"}

        app = App(root_dir, template_engine=mock_template_engine)

        app.template("sample_template", mock_context)

        mock_template_engine.render.assert_called_once_with(
            "sample_template", mock_context
        )
