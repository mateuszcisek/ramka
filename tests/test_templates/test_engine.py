import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from ramka.templates import JinjaTemplateEngine


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


@patch("ramka.templates.engine.os.path.isdir")
@patch("ramka.templates.engine.Environment")
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


@patch("ramka.templates.engine.os.path.isdir")
def test_jinja_engine_render_raises_error_when_template_doesnt_exist(  # pylint: disable=unused-argument
    mock_isdir,
):
    """
    Given a JinjaTemplateEngine
    When I call the `render` method
    And the template that I want to render does not exist
    Then an exception should be raised.
    """
    # pylint: disable=no-member, protected-access
    mock_isdir.return_value = True

    engine = JinjaTemplateEngine("sample_directory")

    with pytest.raises(FileNotFoundError):
        engine.render("sample_template.html")


@patch("ramka.templates.engine.os.path.isdir")
@patch("ramka.templates.engine.Environment")
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


def test_jinja_engine_initialized_with_non_existing_directory():
    """
    When I initialize the JinjaTemplateEngine with non-existing directory
    Then an exception should be raised.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        with pytest.raises(FileNotFoundError):
            JinjaTemplateEngine(os.path.join(root_dir, "non_existing"))


def test_jinja_engine_initialized_with_file_instead_of_directory():
    """
    When I initialize the JinjaTemplateEngine with a file instead of a directory
    Then an exception should be raised.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        file_path = os.path.join(root_dir, "file.txt")
        with open(file_path, "w", encoding="utf-8") as file_:
            file_.write("Hello, world!")

        with pytest.raises(FileNotFoundError):
            JinjaTemplateEngine(file_path)
