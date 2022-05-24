import tempfile
from unittest.mock import Mock, patch

from web_framework.app import App
from web_framework.routing import SimpleRouter
from web_framework.static import WhiteNoiseEngine
from web_framework.templates import JinjaTemplateEngine
from web_framework.views.errors import (
    default_error_handler,
    http_404_not_found,
    http_405_method_not_allowed,
)


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_static_files_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_default_router(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_static_files_engine,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And no router is given as the parameter
    Then the default router should be used.
    """
    app = App("/")

    # pylint: disable=protected-access
    assert isinstance(app._router, SimpleRouter)


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_static_files_engine")
@patch("web_framework.app.App._initialize_middleware")
@patch("web_framework.app.SimpleRouter")
def test_initialize_with_default_router_kwargs(  # pylint: disable=unused-argument
    mock_router,
    mock_initialize_middleware,
    mock_initialize_static_files_engine,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And no router is given as the parameter
    And the router kwargs are given as the parameter
    Then the default router should be used
    And it should be initialized using the given kwargs.
    """
    App("/", router_kwargs={"foo": "bar"})
    mock_router.assert_called_with(foo="bar")


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_static_files_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_custom_router(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_static_files_engine,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And a custom router is given as the parameter
    Then the custom router should be used.
    """
    mock_router = Mock()
    app = App("/", router=mock_router)

    # pylint: disable=protected-access
    assert app._router == mock_router


@patch("web_framework.app.App._initialize_static_files_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_default_template_engine(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_static_files_engine,
):
    """
    When the app is initialized
    And no template engine is given as the parameter
    Then the default template engine should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        app = App(root_dir)

        # pylint: disable=protected-access
        assert isinstance(app._template_engine, JinjaTemplateEngine)


@patch("web_framework.app.App._initialize_static_files_engine")
@patch("web_framework.app.App._initialize_middleware")
@patch("web_framework.app.JinjaTemplateEngine")
def test_initialize_with_default_template_engine_kwargs(  # pylint: disable=unused-argument
    mock_template_engine,
    mock_initialize_static_files_engine,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And no template engine is given as the parameter
    And the template engine kwargs are given as the parameter
    Then the default template engine should be used
    And it should be initialized using the given kwargs.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        App(root_dir, template_engine_kwargs={"foo": "bar"})
        mock_template_engine.assert_called_with(foo="bar")


@patch("web_framework.app.App._initialize_static_files_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_custom_template_engine(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_static_files_engine,
):
    """
    When the app is initialized
    And a custom template engine is given as the parameter
    Then the custom template engine should be used.
    """
    mock_template_engine = Mock()
    app = App("/", template_engine=mock_template_engine)

    # pylint: disable=protected-access
    assert app._template_engine == mock_template_engine


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_static_files_engine(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And static files directory is given as the parameter
    And no static files engine is given as the parameter
    Then the default static files engine should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        app = App(root_dir, static_files_dir=root_dir)

        # pylint: disable=protected-access
        assert isinstance(app._static_files_engine, WhiteNoiseEngine)


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_no_static_files_directory(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And no static files directory is given as the parameter
    Then no static file engine should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        app = App(root_dir)

        # pylint: disable=protected-access
        assert app._static_files_engine is None


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_middleware")
@patch("web_framework.app.WhiteNoiseEngine")
def test_initialize_with_default_static_files_engine_kwargs(  # pylint: disable=unused-argument
    mock_static_files_engine,
    mock_initialize_static_files_engine,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And static files directory is given as the parameter
    And no static files engine is given as the parameter
    And the static files engine kwargs are given as the parameter
    Then the default static files engine should be used
    And it should be initialized using the given kwargs.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        App(
            root_dir,
            static_files_dir=root_dir,
            static_files_engine_kwargs={"foo": "bar"},
        )
        mock_static_files_engine.assert_called_with(foo="bar")


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_custom_static_files_engine(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And a custom static files engine is given as the parameter
    Then the custom static files engine should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        mock_static_files_engine = Mock()
        app = App(
            root_dir,
            static_files_dir=root_dir,
            static_files_engine=mock_static_files_engine,
        )

        # pylint: disable=protected-access
        assert app._static_files_engine == mock_static_files_engine


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_default_404_handler(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And no 404 handler is given as the parameter
    Then the default 404 handler should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        app = App(root_dir)

        # pylint: disable=protected-access, comparison-with-callable
        assert app._http_404_handler == http_404_not_found


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_custom_404_handler(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And a custom 404 handler is given as the parameter
    Then the custom 404 handler should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        mock_404_handler = Mock()
        app = App(root_dir, http_404_not_found_handler=mock_404_handler)

        # pylint: disable=protected-access
        assert app._http_404_handler == mock_404_handler


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_default_405_handler(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And no 405 handler is given as the parameter
    Then the default 405 handler should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        app = App(root_dir)

        # pylint: disable=protected-access, comparison-with-callable
        assert app._http_405_handler == http_405_method_not_allowed


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_custom_405_handler(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And a custom 405 handler is given as the parameter
    Then the custom 405 handler should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        mock_405_handler = Mock()
        app = App(root_dir, http_405_method_not_allowed_handler=mock_405_handler)

        # pylint: disable=protected-access
        assert app._http_405_handler == mock_405_handler


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_default_error_handler(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And no error handler is given as the parameter
    Then the default error handler should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        app = App(root_dir)

        # pylint: disable=protected-access, comparison-with-callable
        assert app._error_handler == default_error_handler


@patch("web_framework.app.App._initialize_template_engine")
@patch("web_framework.app.App._initialize_middleware")
def test_initialize_with_custom_error_handler(  # pylint: disable=unused-argument
    mock_initialize_middleware,
    mock_initialize_template_engine,
):
    """
    When the app is initialized
    And a custom error handler is given as the parameter
    Then the custom error handler should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        mock_error_handler = Mock()
        app = App(root_dir, error_handler=mock_error_handler)

        # pylint: disable=protected-access
        assert app._error_handler == mock_error_handler


@patch("web_framework.app.Middleware")
def test_initialize_middleware_with_no_custom_middleware(mock_middleware):
    """
    When the app is initialized
    And no custom middleware is given as the parameter
    Then only the default middleware should be used.
    """
    with tempfile.TemporaryDirectory() as root_dir:
        app = App(root_dir)

        # pylint: disable=protected-access
        assert app._middleware == mock_middleware.return_value
        mock_middleware.return_value.add.assert_not_called()


@patch("web_framework.app.Middleware")
def test_initialize_middleware_with_custom_middleware(mock_middleware):
    """
    When the app is initialized
    And custom middleware is given as the parameter
    Then the default middleware and the custom middleware should be used.
    """
    mock_second_middleware = Mock()

    with tempfile.TemporaryDirectory() as root_dir:
        App(root_dir, middleware_classes=[mock_second_middleware])

        # pylint: disable=protected-access
        mock_middleware.return_value.add.assert_called_once_with(mock_second_middleware)
