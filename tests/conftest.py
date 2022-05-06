import pytest

from web_framework.test import TestApp


@pytest.fixture
def create_app():
    def _create_app(force_trailing_slashes: bool = False):
        return TestApp(force_trailing_slashes=force_trailing_slashes)

    return _create_app
