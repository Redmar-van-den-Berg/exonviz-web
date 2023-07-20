from flask import Flask
from exonviz.draw import draw_exons
from exonviz.cli import fetch_exons


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> str:
    return "Hello, world!"
