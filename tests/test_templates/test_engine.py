import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from web_framework.templates import JinjaTemplateEngine


@patch("web_framework.templates.engine.os.path.isdir")
def test_jinja_engine_initialized_with_correct_root_dir(mock_os):

    mock_os.path.isdir.return_value = True

    with tempfile.TemporaryDirectory() as root_dir:
        dir_1_path = os.path.join(root_dir, "module_1", "templates", "module_1")
        dir_2_path = os.path.join(root_dir, "module_2", "templates", "module_2")

        os.makedirs(dir_1_path)
        os.makedirs(dir_2_path)

        Path(os.path.join(dir_1_path, "sample_template.html")).touch()
        Path(os.path.join(dir_2_path, "sample_template.html")).touch()

        engine = JinjaTemplateEngine(root_dir)

        assert engine.has_template("module_1/sample_template.html")
        assert engine.has_template("module_2/sample_template.html")
        assert not engine.has_template("sample_template.html")
