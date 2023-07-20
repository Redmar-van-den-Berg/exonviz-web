from flask import Flask
from typing import Tuple, List

from exonviz.draw import draw_exons
from exonviz.cli import fetch_exons
from exonviz.exon import Exon


app = Flask(__name__)


def cache_fetch(transcript: str) -> Tuple[List[Exon], bool]:
    """Wrapper to cache calls to mutalyzer"""
    return fetch_exons(transcript)


@app.route("/", methods=["GET"])
def index() -> str:
    return 'Try it out!: <a href="http://127.0.0.1:5000/draw/NG_012337.3(NM_003002.4):c.274G>T">Click</a>'


@app.route("/draw/<transcript>", methods=["GET"])
def draw(transcript: str) -> str:
    exons, reverse = cache_fetch(transcript)
    return str(draw_exons(exons, reverse))
