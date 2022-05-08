import os

from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter

from web_framework.app import App


class TestSession(RequestsSession):
    def __init__(self, base_url: str, adapter: RequestsWSGIAdapter):
        super().__init__()
        self._base_url = base_url
        self.mount(prefix=self._base_url, adapter=adapter)

    @property
    def base_url(self) -> str:
        return self._base_url.rstrip("/")

    def _request(self, method, url, **kwargs):
        func = getattr(super(), method)
        if not func:
            raise AttributeError(f"Method {method} not supported.")

        url = url.lstrip("/")
        return func(f"{self.base_url}/{url}", **kwargs)

    def get(self, url, **kwargs):
        return self._request("get", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self._request("post", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self._request("put", url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self._request("patch", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self._request("delete", url, **kwargs)


class TestApp(App):
    def __init__(self, *, base_url: str = "http://testserver"):
        super().__init__(
            root_dir=os.getcwd(),
        )
        self._base_url = base_url

    @property
    def test_session(self):
        return TestSession(self._base_url, RequestsWSGIAdapter(self))
