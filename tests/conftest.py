import pytest
from requests import Session as RequestsSession

from web_framework.test import TestApp


def _create_app(force_trailing_slashes: bool = False) -> TestApp:
    return TestApp(force_trailing_slashes=force_trailing_slashes)


@pytest.fixture
def create_app():
    return _create_app


@pytest.fixture
def create_session():
    def _create_session(
        app: TestApp = None, force_trailing_slashes: bool = False
    ) -> RequestsSession:
        if not app:
            app = _create_app(force_trailing_slashes=force_trailing_slashes)

        return app.test_session

    return _create_session
