from flask import Blueprint, Flask, render_template
from typing import Tuple, List

from exonviz.draw import draw_exons
from exonviz.cli import fetch_exons
from exonviz.exon import Exon


app = Flask(__name__)
bp = Blueprint("exonviz", __name__)
app.register_blueprint(bp)


def cache_fetch(transcript: str) -> Tuple[List[Exon], bool]:
    """Wrapper to cache calls to mutalyzer"""
    return fetch_exons(transcript)


@app.route("/", methods=["GET"])
def index() -> str:
    return render_template("index.html")


@app.route("/draw/<transcript>", methods=["GET"])
def draw(transcript: str) -> str:
    exons, reverse = cache_fetch(transcript)
    return str(draw_exons(exons, reverse))
