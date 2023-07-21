from flask import Blueprint, Flask, render_template, session, request
from typing import Tuple, List

from exonviz import draw_exons
from exonviz import fetch_exons
from exonviz import Exon


app = Flask(__name__)
bp = Blueprint("exonviz", __name__)
app.register_blueprint(bp)


def cache_fetch(transcript: str) -> Tuple[List[Exon], bool]:
    """Wrapper to cache calls to mutalyzer"""
    return fetch_exons(transcript)


@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


@app.route("/", methods=["POST"])
def index_post() -> str:
    text = request.form["text"]
    exons, reverse = cache_fetch(text)
    session["svg"] = str(draw_exons(exons, reverse))
    return render_template("index.html")


@app.route("/draw/<transcript>", methods=["GET"])
def draw(transcript: str) -> str:
    exons, reverse = cache_fetch(transcript)
    return str(draw_exons(exons, reverse))


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.run()
