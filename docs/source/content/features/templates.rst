Templates
=========

The templates are used to generate HTML pages and return them as the response
to the clients. A template engine is used to render the templates.

By default, the template engine is :py:class:`ramka.templates.JinjaTemplateEngine`
(it uses `Jinja2 <https://jinja.palletsprojects.com/>`_ under the hood), but you
can change it by setting the ``template_engine`` parameter while initializing
the application. Each custom template engine should have two methods
implemented:

* ``render`` method that takes a template name and a *context* dictionary as
  arguments and returns the rendered template,
* ``has_template`` method that takes a template name as argument and returns
  ``True`` if the template exists and ``False`` otherwise.

By default, all templates from directories called ``templates`` will be loaded
and available for rendering. To override the default engine settings, set the
``template_engine_kwargs`` dictionary while initializing the application, the
following settings can be used:

* ``root_dir`` - the root directory where the templates are located, it's
  usually the same as the root directory of the application (see
  section :doc:`application` to learn more).
* ``template_dir_name`` - the name of the directory that contains the templates
  (defaults to ``templates``).


Example usage
-------------

Here is an example code that shows how to use the template engine to render a
template in a view:

.. code-block:: python

    @app.route("/")
    def home(request, response):
        response.body = app.template("sample_routes/home.html")


The code above will render the template ``templates/sample_routes/home.html``.
This is how the file structure looks like in the example:

.. code-block::

   sample_routes
   ├── __init__.py
   ├── app.py
   └── templates
      └── sample_routes
         └── home.html

You can group the templates into subdirectories to make your application more
readable.


Reference implementation
------------------------

For a reference implementation of the static files engine, see class
:py:class:`ramka.templates.engine.JinjaTemplateEngine`.
