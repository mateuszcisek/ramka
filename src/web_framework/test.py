from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from web_framework.app import App
from web_framework.routing.resolver import BaseRouteResolver


class TestSession(RequestsSession):
    def __init__(self, base_url: str, adapter: RequestsWSGIAdapter):
        super().__init__()
        self._base_url = base_url
        self.mount(prefix=self._base_url, adapter=adapter)

    @property
    def base_url(self) -> str:
        return self._base_url.rstrip("/")

    def _format_path(self, path: str) -> str:
        return path.lstrip("/")

    def _request(self, method, path, *args, **kwargs):
        func = getattr(super(), method)
        if not func:
            raise AttributeError("Method %s not supported." % method)

        return func(f"{self.base_url}/{self._format_path(path)}", *args, **kwargs)

    def get(self, path, *args, **kwargs):
        return self._request("get", path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self._request("post", path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        return self._request("put", path, *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        return self._request("patch", path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self._request("delete", path, *args, **kwargs)


class TestApp(App):
    def __init__(self, *, base_url: str = "http://testserver"):
        super().__init__()
        self._base_url = base_url

    @property
    def test_session(self):
        return TestSession(self._base_url, RequestsWSGIAdapter(self))
