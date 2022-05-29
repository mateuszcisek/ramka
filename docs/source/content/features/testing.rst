Testing
=======

*ramka* provides very basic tools for testing your application.

Class :py:class:`ramka.test.TestSession` extends the ``Session`` class from
the `requests <https://requests.readthedocs.io/>`_ package. It provides a few
additional methods for testing HTTP requests.

Function :py:func:`ramka.test.create_test_app` can be used to add a test session
property to your custom application.


Example usage
-------------

Let's take a look at a very simple example of how we can test our app with
`pytest <https://pytest.org/>`_.

This is a sample application:

.. code-block:: python

  import os

  from ramka.app import App

  app = App(root_dir=os.path.dirname(os.path.realpath(__file__)))

  @app.route("/")
  def text(response, response):
      response.text = "Hello!"


Here is a sample ``conftest.py`` file:

.. code-block:: python

   import os

   import pytest

   from examples.sample_routes.app import App
   from ramka.test import TestSession, create_test_app

   @pytest.fixture(name="create_session")
   def create_session_fixture():
       def _create_session(app: App) -> TestSession:
           if not hasattr(app, "test_session"):
               app = create_test_app(app)
   
           return app.test_session

       return _create_session

And this is a sample test:

.. code-block:: python

   import pytest

   from examples.sample_routes.app import app

   def test_home(create_session):
       session = create_session(app)
       response = session.get("/")
   
       assert response.status_code == 200
       assert response.text == "Hello!"

And now, let's break it down.

First, the app. It's very simple, there's only one route that returns a simple
test in the response.

Next, we have a fixture. The purpose of that fixture is to create the
``test_session`` property in the application (if it's not there yet). It returns
a function and we should call it with the application that we want to test as
the argument.

Then we have the test. First, we import the app that we want to test. Then,
in the test, we create a test session in that app. Finally, we can call perform
a ``GET`` request on the ``/`` route and check the response.

I admit that this may not be the most elegant way to test an app, but hey, it's
not that bad, it works, and I'll try to improve it in the future.


Reference implementation
------------------------

There are some example tests implemented for the sample application in the
repository. See :py:mod:`examples.sample_routes.tests` for more information.
