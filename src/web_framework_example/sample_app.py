import os

from web_framework.app import App

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "static")


app = App(
    root_dir=ROOT_DIR,
    # Directory where the static files are located.
    static_dir=STATIC_DIR,
)


@app.route("/")
def home(_, response):
    response.text = "Hello from the HOME page"


@app.route("/about")
def about(_, response):
    response.text = "Hello from the ABOUT page"


@app.route("/hello/{name}/")
def hello(_, response, name):
    response.text = f"Hello {name}"


@app.route("/sum/{first_number:d}/{second_number:d}/")
def sum_view(_, response, first_number, second_number):
    response.text = f"Sum {first_number + second_number}"


@app.route("/book")
class BooksResource:
    def get(self, _, response):  # pylint: disable=no-self-use
        response.text = "Books Page"

    def post(self, _, response):  # pylint: disable=no-self-use
        response.text = "Endpoint to create a book"


def another_route(_, response):
    response.text = "Another route"


app.add_route("/another_route", another_route)


@app.route("/html/")
def html(_, response):
    response.body = app.template("sample/template.html")
