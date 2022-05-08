import pytest
from requests import Session as RequestsSession

from web_framework.routing.resolver import SimpleRouteResolver
from web_framework.test import TestApp
from web_framework.views.base_view import BaseView


@pytest.fixture
def app():
    return TestApp()


@pytest.fixture
def create_session():
    def _create_session(app: TestApp = None,) -> RequestsSession:
        if not app:
            app = TestApp()

        return app.test_session

    return _create_session


@pytest.fixture
def sample_class_view():
    class SampleView(BaseView):
        def get(self, request, response):
            response.text = "Hello, world!"

    return SampleView


@pytest.fixture
def sample_func_view():
    def sample_view(self, request, response):
        response.text = "Hello, world!"

    return sample_view
