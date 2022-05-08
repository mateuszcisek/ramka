import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, Template
from jinja2.exceptions import TemplateNotFound


class BaseTemplateEngine(ABC):

    def __init__(self, root_dir: str = None, template_dir_name: Optional[str] = "templates"):
        self._root_dir = root_dir
        self._template_dir_name = template_dir_name

    @abstractmethod
    def render(self, template_name: str, context: Optional[Dict] = None) -> Any:
        pass


class Jinja2TemplateEngine(BaseTemplateEngine):
    def __init__(self, root_dir: str = None, template_dir_name: Optional[str] = "templates"):
        super().__init__(root_dir, template_dir_name)

        if not self._root_dir or not os.path.isdir(self._root_dir):
            raise FileNotFoundError(f"{self._root_dir} is not a directory.")

        self._env = Environment(
            loader=FileSystemLoader(
                self._find_template_directories(root_dir, template_dir_name)
            )
        )

    def _find_template_directories(
        self, root_dir: str, template_dir_name: str
    ) -> List[str]:
        result = []
        for rootdir, dirs, _ in os.walk(root_dir):
            for subdir in dirs:
                if subdir == template_dir_name:
                    result.append(os.path.join(rootdir, subdir))

        return result

    def render(self, template_name: str, context: Optional[Dict] = None) -> Template:
        if context is None:
            context = {}

        try:
            return self._env.get_template(template_name).render(**context).encode()
        except TemplateNotFound as ex:
            raise FileNotFoundError(f"{template_name} is not found.") from ex
