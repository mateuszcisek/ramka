import pytest

from ramka.views.base_view import BaseView


@pytest.fixture(name="sample_class_view")
def sample_class_view_fixture():
    """Return a sample class-based view."""

    class SampleView(BaseView):
        """Simple class-based view with one HTTP method implemented."""

        def get(  # pylint: disable=no-self-use,unused-argument
            self, request, response, **kwargs
        ) -> None:
            response.text = "Hello, world!"

    return SampleView


@pytest.fixture(name="sample_func_view")
def sample_func_view_fixture():
    """Return a sample function-based view."""

    def sample_view(  # pylint: disable=no-self-use,unused-argument
        request, response
    ) -> None:
        response.text = "Hello, world!"

    return sample_view
