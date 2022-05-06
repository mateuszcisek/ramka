from web_framework.app import App

from requests import Session as RequestsSession
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter


class TestApp(App):

    def test_session(self, base_url="http://testserver"):
        session = RequestsSession()
        session.mount(prefix=base_url, adapter=RequestsWSGIAdapter(self))
        return session
