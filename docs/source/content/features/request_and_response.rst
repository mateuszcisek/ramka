Request and response
====================

When it comes to the request and response classes, there are custom classes for
both (:py:class:`ramka.request.Request` and
:py:class:`ramka.response.Response`), but those classes inherit from ``Request``
and ``Response`` from ``webob`` library respectively and there is no custom
logic in any of them at the moment. Because of that, there's no point to
describe it here. If you want to learn more about that library and how it works,
you can read the documentation at `WebOb documentation
<https://docs.pylonsproject.org/projects/webob/en/stable/>`_.
