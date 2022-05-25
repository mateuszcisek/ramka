from unittest.mock import Mock, patch

from web_framework.views.errors import (
    _error_page,
    default_error_handler,
    http_404_not_found,
    http_405_method_not_allowed,
)


def test_error_page():
    """
    Given a request
    When I call the _error_page function
    Then the response object should be updated with correct data.
    """
    mock_response = Mock()

    _error_page(mock_response, 404, "Not found.")

    assert mock_response.status_code == 404
    assert mock_response.content_type == "application/json"
    assert mock_response.text == '{"error": "Not found."}'


@patch("web_framework.views.errors._error_page")
def test_http_404_not_found(mock_error_page):
    """
    Given a response object
    When I call the http_404_not_found function
    Then the _error_page function should be called with correct parameters.
    """
    mock_response = Mock()
    http_404_not_found(Mock(), mock_response)

    mock_error_page.assert_called_once_with(mock_response, 404, "Not found.")


@patch("web_framework.views.errors._error_page")
def test_http_405_not_found(mock_error_page):
    """
    Given a response object
    When I call the http_405_method_not_allowed function
    Then the _error_page function should be called with correct parameters.
    """
    mock_response = Mock()
    http_405_method_not_allowed(Mock(), mock_response)

    mock_error_page.assert_called_once_with(mock_response, 405, "Method not allowed.")


@patch("web_framework.views.errors._error_page")
def test_default_error_handler(mock_error_page):
    """
    Given a response object
    When I call the default_error_handler function
    Then the _error_page function should be called with correct parameters.
    """
    mock_response = Mock()
    default_error_handler(Mock(), mock_response, ValueError("An error occurred."))

    mock_error_page.assert_called_once_with(mock_response, 500, "An error occurred.")
