Application
===========

To create a new application, simply create a new object of class
:py:class:`ramka.app.App`. You need to specify the root directory of your app
manually (I know it's not perfect, it will be fixed in the future). Here is an
example:

.. code-block:: python

   import os
   from ramka.app import App

   app = App(root_dir=os.path.dirname(os.path.realpath(__file__)))

Apart from ``root_dir``, you can also specify the following parameters (all of
them are optional):

* ``router`` - the router to use (see more about routing in section
  :doc:`routing`), the default value is :py:class:`ramka.routing.SimpleRouter`.
* ``router_kwargs``- the kwargs to pass to the default router if the router has
  not been defined (see the ``router`` parameter).
* ``template_engine`` - the template engine to use (see more about templates in
  section :doc:`templates`), the default value is
  :py:class:`ramka.templates.JinjaTemplateEngine`.
* ``template_engine_kwargs`` - the kwargs to pass to the default template engine
  if the engine has not been defined (see the ``template_engine`` parameter).
  If defined, it should also contain a ``root_dir`` parameter.
* ``static_files_dir`` - the directory containing static files. It needs to be
  defined if you want to use static files.
* ``static_files_engine`` - the static file engne to use (see more about static
  files in section :doc:`static_files`), the default value is
  :py:class:`ramka.static.WhiteNoiseEngine`.
* ``static_files_engine_kwargs`` - the kwargs to pass to the default static
  files engine if the engine has not been defined (see the
  ``static_files_engine`` parameter).
* ``http_404_not_found_handler`` - the handler to use for handling HTTP 404
  errors, the default value is :py:func:`ramka.views.http_404_not_found`.
* ``http_405_method_not_allowed_handler`` - the handler to use for HTTP 405
  errors, the default value is :py:func:`ramka.views.http_405_method_not_allowed`.
* ``error_handler`` - the handler to use for handling other errors, the
  default value is :py:func:`ramka.views.default_error_handler`.
* ``middleware_classes``- the list of the middleware classes to use. The default
  middleware (:py:class:`ramka.middleware.Middleware`) is always loaded
  automatically, so you don't need to specify it.

``app`` is a WSGI app so it can be used with any WSGI HTTP server (such as
Gunicorn). See section :doc:`../usage` for more information.

``App`` class also provides some helper methods for working with routes and
templates:

* ``add_route`` can be used to add a route specified somewhere else in the code
  I can be either a function or a class that inherits from
  :py:class:`ramka.views.BaseView`. Sample usages:

  .. code-block:: python

     def sample_function_view(request, response):
         response.text = "External route"

     app.add_route("/function-view", sample_function_view)


     class SampleClassView(BaseView): 
         def get(self, request, response, **kwargs):
             response.text = "Sample class-view GET page"

     app.add_route("/class-view", SampleClassView)

* ``route`` provides the same functionality as ``add_route`` but it is meant to
  be used as a decorator, for example:

  .. code-block:: python

     @app.route("/function-view")
     def sample_function_view(request, response):
         response.text = "External route"

     @app.route("/class-view")
     class SampleClassView(BaseView): 
         def get(self, request, response, **kwargs):
             response.text = "Sample class-view GET page"

* ``has_route`` can be used to check if a route with a given path has been
  already defined.

* ``template`` method can be used to render a template. It takes the template
  name and the context as parameters. The context is a dictionary that will be
  passed to the template engine. Sample usage:

  .. code-block:: python

     @app.route("/")
     def home(request, response):
         response.body = app.template(
             "sample_routes/home.html", {"name": "John"}
         )

Methods ``add_route``, ``route``, and ``has_route`` use a router object
underneath and the same functionality can be achieved by using the router object
directly and then pass it to the ``App`` as a parameter.

The same applies to the ``template`` method but in that case it uses a template
engine object under the hood.
