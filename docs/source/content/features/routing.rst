Routing
=======

Routing is the process of determining how to handle a request to a particular
URL. In *ramka* it is done using two components: routes that define views that
are rendered for specified URLs and a router that is responsible for determining
which route should be used for a given request.


Router
------

The default router used in the app is the :py:class:`ramka.routers.SimpleRouter`.
You can override it by setting the ``router`` parameter while initializing the
application. Each router should inherit the :py:class:`ramka.routers.BaseRouter`
class and implement the following methods:

* ``add_route`` - adds a route to the router. It accepts a route path
  (a string), a view (a function or a class, see :doc:`views` to learn more),
  and methods that should be allowed for the route (a list of strings). See
  the examples below:

  .. code-block:: python

     def sample_function_view(request, response):
         response.text = "External route"

     app.add_route("/function-view", sample_function_view, methods=["GET"])


     class SampleClassView(BaseView): 
         def get(self, request, response, **kwargs):
             response.text = "Sample class-view GET page"

     app.add_route("/class-view", SampleClassView, methods=["GET", "POST"])

* ``route`` provides the same functionality as ``add_route`` but it is meant to
  be used as a decorator and therefore does not accept the view as the
  parameter. For example:

  .. code-block:: python

     @app.route("/function-view", methods=["GET"])
     def sample_function_view(request, response):
         response.text = "External route"

     @app.route("/class-view", methods=["GET", "POST"])
     class SampleClassView(BaseView): 
         def get(self, request, response, **kwargs):
             response.text = "Sample class-view GET page"

* ``has_route`` can be used to check if a route with a given path has been
  already defined. It only takes a path as a parameter and returns a boolean.

* ``resolve`` takes a path and returns a :py:class:`ramka.routing.ResolvedRoute`
  object that is described in the next section.

In all examples above the methods from ``app`` objects are used, but under the
hood they call the methods from the router. All those methods can be used
directly on the router object.


Routes and Resolved Routes
--------------------------

Functions ``add_route`` and ``route`` described above create
:py:class:`ramka.routing.Route` objects underneath. These objects are used to store
information about the route and to provide a way to resolve the route for a
given request. When a route is resolved by the router it returns a
:py:class:`ramka.routing.ResolvedRoute` object. The only difference between the two
is that the resolved route also contains resolved dynamic parameters of the
route for the request.

For example, let's take a look at the code below:

.. code-block:: python

    @app.route("/hello/{name}")
    def sample_function_view(request, response, name):
        response.text = f"Hello {name}!"

When the router resolves the route, it returns a
:py:class:`ramka.routing.ResolvedRoute` object that contains resolved ``name``
parameter with the value.

If you want to use custom implementations of ``Route`` and ``ResolvedRoute``
classes then you can do that in your custom router. In the ``SimpleRouter``,
the ``Route`` and ``ResolvedRoute`` objects are created in ``add_route`` and
``resolve`` methods, so you can replace them with your own implementations.


Reference implementation
------------------------

For a reference implementation of the router, see
:py:class:`ramka.routing.SimpleRouter` in file
:py:mod:`ramka.routing.router`. Both :py:class:`ramka.routing.Route` and
:py:class:`ramka.routing.ResolvedRoute` classes are defined in file
:py:mod:`ramka.routing.route`.
