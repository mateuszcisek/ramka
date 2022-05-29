A very small Python web framework
======================================

*ramka* (a Polish word for a small frame) is a very simple web framework written
in Python. It is based on a very good course
`Building Your Own Python Web Framework <https://testdriven.io/courses/python-web-framework/>`_
by `testdriven.io <https://testdriven.io/>`_ which I highly recommend.

Please bear in mind that at the moment only very basic functionality is
implemented and that this framework is far from being finished. Having said
that, I do have some ideas for the future.

At the moment, you can define some routes and then serve the content (HTML,
text, JSON) to the client. You can use dynamic routes and serve templates and
static files (like stylesheets and images). And that's it. A framework is
probably a big word for it but there is some potential for it to grow.

As I said it's still a work in progress. Some features I am planning to add:

* database support - there are no plans to implement custom ORM, but integrating
  one of the existing ones (like SQLAlchemy) is probably a good start,
* authentication - it can use databases or some different method,
* plugins - the goal is to add a plugin mechanism and add more features as
  installable plugins.

There will be probably more but it's difficult for me to say at the moment.
Anyway, I would treat this as a learning project rather than a real framework.
Feel free to try it out and send me any feedback.

Contents
--------

.. toctree::
   :maxdepth: 2

   content/installation
   content/usage
   content/features/index
   content/source_code/modules
