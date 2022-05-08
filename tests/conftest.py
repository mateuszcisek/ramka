import pytest
from requests import Session as RequestsSession

from web_framework.test import TestApp
from web_framework.views.base_view import BaseView


@pytest.fixture(name="app")
def app_fixture():
    return TestApp()


@pytest.fixture(name="create_session")
def create_session_fixture():
    def _create_session(app: TestApp = None) -> RequestsSession:
        if not app:
            app = TestApp()

        return app.test_session

    return _create_session


@pytest.fixture(name="sample_class_view")
def sample_class_view_fixture():
    class SampleView(BaseView):
        def get(self, _, response):  # pylint: disable=no-self-use
            response.text = "Hello, world!"

    return SampleView


@pytest.fixture(name="sample_func_view")
def sample_func_view_fixture():
    def sample_view(_, response):
        response.text = "Hello, world!"

    return sample_view
