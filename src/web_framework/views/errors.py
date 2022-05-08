import json


def _error_page(response, error_code, message):
    response.status_code = error_code
    response.content_type = "application/json"
    response.text = json.dumps({"error": message})


def http_404(_, response):
    _error_page(response, 404, "Not found.")


__all__ = ["http_404"]
