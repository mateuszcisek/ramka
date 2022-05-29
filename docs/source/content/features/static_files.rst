Static files
============

Static files are all images, stylesheets, and JavaScript files and other files
that are not used by the application directly, but can included in the views
and templates. The static files engine is used to serve these files.

To use the static files engine, you need to specify parameter
``static_files_dir`` while initializing the application object. When you add
it to a fact that also ``root_dir`` is required, this is how the app can be
initialized using a ``static`` directory for the static files:

.. code-block:: python

   import os

   from ramka.app import App

   ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
   STATIC_DIR = os.path.join(ROOT_DIR, "static")

   app = App(
       # Root application directory.
       root_dir=ROOT_DIR,
       # Directory where the static files are located.
       static_files_dir=STATIC_DIR,
   )

By default, the static files engine is :py:class:`ramka.static.WhiteNoiseEngine`
(it uses the ``whitenoise`` library under the hood) but you can change it by
setting ``static_files_engine`` parameter while initializing the application.
Each custom engine should have two methods implemented:

* ``__call__`` - should return a WSGI application that serves the static files,
* ``has_file`` - should return ``True`` if the file exists.

The default behavior of the static files engine can be changed by setting
``static_files_engine_kwargs`` parameter while initializing the application.
Here are the options that can be used:

* ``app`` - the application object. This is required.
* ``root_dir`` - the directory with the static files. This is required.
* ``prefix`` - the prefix of the static files. By default it is ``/static`` and
  it means that the URL of all static files will be prefixed with ``/static``.


Example usage
-------------

Let's take the application defined above and the following structure of the
project:

.. code-block::

   sample_app
   ├── __init__.py
   ├── app.py
   ├── static
   |   └── sample_app
   │       └── main.css
   └── templates
       └── sample_app
           └── home.html

We will be able to access file ``main.css`` at the URL
``/static/sample_app/main.css``. That means that we can add the following line
in the ``home.html`` template

.. code-block:: html

   <link rel="stylesheet" href="/static/sample_app/main.css">


Reference implementation
------------------------

For a reference implementation of the static files engine, see class
:py:class:`ramka.static.engine.WhiteNoiseEngine`.
