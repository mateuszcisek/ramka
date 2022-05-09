from abc import ABC


class BaseView(ABC):  # pylint: disable=too-few-public-methods
    """Base class for all class-based views.

    A class-based view is a view that is defined by a class. It defines methods for all
    supported request methods.
    """


__all__ = ["BaseView"]
