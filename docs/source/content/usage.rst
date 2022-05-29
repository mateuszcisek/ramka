Usage
=====

Once installed, you can use *ramka* in your project. There is a very simple
application example in the 
`examples <https://github.com/mateuszcisek/ramka/tree/master/examples>`_
directory in the repository.

Long story short, here is how you can create a very simple app (save it in file
``app.py``):

.. code-block:: python

   import os
   from ramka.app import App

   app = App(root_dir=os.path.dirname(os.path.realpath(__file__)))

   @app.route("/")
   def home(request, response):
       """A very simple example of a view."""
       response.text = "Hello!"

   @app.route("/hello/{name}/")
   def hello(request, response, name):
       """A view with a dynamic argument."""
       response.text = f"Hello {name}!"

And that's it! Now you have a web app with two views. To test it out, you'll
need a web server (for example `Gunicorn <https://gunicorn.org/>`_). To start
the app, just run this command:

.. code-block:: bash

   gunicorn app:app

You should see something like this in your terminal:

.. code-block:: bash

   [INFO] Starting gunicorn 20.1.0
   [INFO] Listening at: http://127.0.0.1:8000 (30642)
   [INFO] Using worker: sync
   [INFO] Booting worker with pid: 30643

And now you can visit `http://127.0.0.1:8000 <http://127.0.0.1:8000>`_ in your
browser to see that it works (you will see ``Hello!``). There's also another
view (the one with a dynamic argument) which you can access by visiting eg.
`http://127.0.0.1:8000/hello/world/ <http://127.0.0.1:8000/hello/world/>`_ and
you'll see ``Hello world!``.

And that's it. As mentioned above, there's a very simple application example in
the `repository <https://github.com/mateuszcisek/ramka/tree/master/examples>`_.
