import json


def _error_page(response, error_code, message):
    response.status_code = error_code
    response.content_type = "application/json"
    response.text = json.dumps({"error": message})


def http_404(_, response):
    _error_page(response, 404, "Not found.")


def default_error_handler(_, response, error: Exception):
    _error_page(response, 500, str(error))


__all__ = ["default_error_handler", "http_404"]
