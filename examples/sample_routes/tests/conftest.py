import os

import pytest

from examples.sample_routes.app import App
from ramka.test import TestSession, create_test_app


@pytest.fixture(name="app")
def app_fixture():
    """Return a test app."""
    return create_test_app(App(root_dir=os.getcwd()))


@pytest.fixture(name="create_session")
def create_session_fixture():
    """Return a function that can be used for creating a new session."""

    def _create_session(app: App = None) -> TestSession:
        if not app:
            app = create_test_app(App(root_dir=os.getcwd()))
        elif not hasattr(app, "test_session"):
            app = create_test_app(app)

        return app.test_session

    return _create_session
