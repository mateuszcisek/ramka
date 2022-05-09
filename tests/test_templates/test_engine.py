import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from web_framework.templates import JinjaTemplateEngine


def test_jinja_engine_initialized_with_correct_root_dir():
    """
    Given two directories with templates and a JinjaTemplateEngine
    When I initialize the engine
    Then all templates should be registered by the engine.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        # Given
        dir_1_path = os.path.join(root_dir, "module_1", "templates", "module_1")
        dir_2_path = os.path.join(root_dir, "module_2", "templates", "module_2")

        os.makedirs(dir_1_path)
        os.makedirs(dir_2_path)

        Path(os.path.join(dir_1_path, "sample_template.html")).touch()
        Path(os.path.join(dir_2_path, "sample_template.html")).touch()

        # When
        engine = JinjaTemplateEngine(root_dir)

        # Then
        assert engine.has_template("module_1/sample_template.html")
        assert engine.has_template("module_2/sample_template.html")
        assert not engine.has_template("sample_template.html")


@patch("web_framework.templates.engine.os.path.isdir")
@patch("web_framework.templates.engine.Environment")
@pytest.mark.parametrize(
    "actual_context, expected_call_kwargs",
    (
        ({"a": 1}, {"a": 1}),
        (None, {}),
    ),
)
def test_jinja_engine_render_calls_correct_methods(  # pylint: disable=unused-argument
    mock_enviroment, mock_isdir, actual_context, expected_call_kwargs
):
    """
    Given a JinjaTemplateEngine
    When I call the `render` method
    Then the `get_template` method should be called with the correct arguments
    And the `render` method should be called with the correct arguments.
    """
    # pylint: disable=no-member, protected-access
    mock_isdir.return_value = True

    engine = JinjaTemplateEngine("sample_directory")
    engine.render("sample_template.html", actual_context)

    engine._env.get_template.assert_called_once_with("sample_template.html")
    engine._env.get_template.return_value.render.assert_called_once_with(
        **expected_call_kwargs
    )


@patch("web_framework.templates.engine.os.path.isdir")
@patch("web_framework.templates.engine.Environment")
def test_jinja_engine_has_template_calls_correct_method(  # pylint: disable=unused-argument
    mock_enviroment, mock_isdir
):
    """
    Given a JinjaTemplateEngine
    When I call the `has_template` method
    Then the `list_templates` method should be called.
    """
    # pylint: disable=no-member, protected-access
    mock_isdir.return_value = True

    engine = JinjaTemplateEngine("sample_directory")
    engine.has_template("sample_template.html")

    engine._env.loader.list_templates.assert_called_once()
