import os

from web_framework.app import App

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "static")
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")


app = App(
    # Trailing slashes will be forced for all routes.
    force_trailing_slashes=True,
    # Directory where the templates are located.
    templates_dir=TEMPLATES_DIR,
    # Directory where the static files are located.
    static_dir=STATIC_DIR,
)


@app.route("/")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"


@app.route("/hello/{name}/")
def hello(request, response, name):
    response.text = f"Hello {name}"


@app.route("/sum/{a:d}/{b:d}/")
def sum(request, response, a, b):
    response.text = f"Sum {a + b}"


@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"


def another_route(req, resp):
    resp.text = "Another route"


app.add_route("/another_route", another_route)


@app.route("/html/")
def sum(req, resp):
    resp.body = app.template("index.html").encode()
