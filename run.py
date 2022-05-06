import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src"))

from web_framework.api import API


app = API(force_trailing_slashes=True)


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
