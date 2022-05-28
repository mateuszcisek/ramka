import os

from ramka.app import App
from ramka.views import BaseView

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "static")


app = App(
    # Root application directory.
    root_dir=ROOT_DIR,
    # Directory where the static files are located.
    static_files_dir=STATIC_DIR,
)


@app.route("/")
def home(_, response):
    """Sample template route. It will render a page using predefined template."""
    response.body = app.template("sample_routes/home.html")


@app.route("/text/")
def text(_, response):
    """The home route. It renders a page with a sample text."""
    response.text = "Hello!"


@app.route("/hello/{name}/")
def hello(_, response, name):
    """Sample route with a dynamic parameter that will be used to render the page."""
    response.text = f"Hello {name}!"


@app.route("/add/{first_number:d}/{second_number:d}/")
def add(_, response, first_number, second_number):
    """Sample route with a dynamic parameters that of which sum will be rendered."""
    response.text = f"Sum: {first_number + second_number}"


@app.route("/limited-view/", methods=["get", "post"])
def limited_view(request, response):
    """Sample route with supported methods specified."""
    response.text = f"HTTP method: {request.method}!"


@app.route("/class-view/")
class SampleClassView(BaseView):
    """Sample class-based view with two methods implemented."""

    def get(  # pylint: disable=no-self-use,unused-argument
        self, request, response, **kwargs
    ):
        response.text = "Sample class-view GET page"

    def post(  # pylint: disable=no-self-use,unused-argument
        self, request, response, **kwargs
    ):
        response.text = "Sample class-view POST page"


def external(_, response):
    """
    Sample route that is defined outside of the app and is added to the router later.
    """
    response.text = "External route"


app.add_route("/external", external)
