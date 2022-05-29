Views
=====

In *ramka*, you can define the views in the application as both functions and
classes.

In both cases, there are two objects that will be passed to your views:
``request`` and ``response``. The ``request`` object is an instance of
:py:class:`ramka.request.Request`, and the ``response`` object is an instance of
:py:class:`ramka.response.Response`. See more about those classes in section
:doc:`request_and_response`.


Function-based views
--------------------

Function-based views are essentially just functions that take ``request`` and
``response`` objects as arguments. They are the simplest way to define views.

If you have dynamic parameters in the route that points to a function then
the function should also accept those parameters.

See the code below for an example:

.. code-block:: python

   @app.route("/hello/{name}/", methods=["GET", "POST"])
   def hello(request, response, name):
       # Use request.method to access the HTTP method
       response.text = f"Hello {name}!"

By default, only GET requests are allowed. To allow other methods, you can
specify the ``methods`` argument in the decorator.


Class-based views
-----------------

Class-based views may be a good choice for handling more than one HTTP method
(GET, POST, PUT, DELETE, etc.) with nice separation of logic for each method.

Let's take a look at the example below:

.. code-block:: python

   @app.route("/class-view/")
   class SampleClassView(BaseView):

       def get(self, request, response, **kwargs):
           response.text = "Sample class-view GET page"

       def post(self, request, response, **kwargs):
           response.text = "Sample class-view POST page"

Each class-based view should inherit from :py:class:`ramka.views.BaseView`. You can
specify a separate method for each HTTP method that you want to handle. Only
implemented methods will be supported, and the rest will return a response
with HTTP code 405 (*Method Not Allowed*).

If you define dynamic parameters in the routes then they will be passed in the
``kwargs`` dictionary to the methods.
