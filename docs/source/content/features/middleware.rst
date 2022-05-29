Middleware
==========

Middleware can be used to modify both request and/or response. It may be used
for authentication, logging, or other purposes.

In *ramka*, there is only one middleware defined by default, and it does not
modify anything. It's only purpose is to enable other middleware classes to be
used.

All middleware classes should inherit from :py:class:`ramka.middleware.Middleware`
and implement one or both of the following methods:

* ``process_request`` - called before the request is processed and accepts one
  argument, the request object.
* ``process_response`` - called after the request is processed and accepts two
  arguments, the request object and the response object.

Middlewares can be passed to the application using the ``middleware_classes``
keyword.


Reference implementation
------------------------

At the moment, there is no reference implementation in the repository. Let's
take a look at the code below:

.. code-block:: python

   import os

   from ramka.app import App
   from ramka.middleware import Middleware

   ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


   class SampleMiddleware(Middleware):

       def process_response(self, request, response) -> None:
           response.text = f"Updated: {response.text}"
 

   app = App(
       root_dir=ROOT_DIR,
       middleware_classes=[SampleMiddleware],
   )

In this example, the ``SampleMiddleware`` class modifies the response text.
Obviously this is not a real use case, but it's a good example of how to use
middleware. The ``process_request`` method is not implemented, but you can
easily implement it if you need to.

