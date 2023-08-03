from flask import Blueprint, Flask, render_template, session, request, flash
from typing import Tuple, List, Dict, Any
import math
import secrets
import functools

from exonviz import draw_exons, config
from exonviz import fetch_exons
from exonviz import Exon


app = Flask(__name__)
bp = Blueprint("exonviz", __name__)
app.register_blueprint(bp)
app.secret_key = secrets.token_hex()


@functools.cache
def cache_fetch(transcript: str) -> Tuple[List[Exon], bool]:
    """Wrapper to cache calls to mutalyzer"""
    app.logger.info(f"Fetching {transcript} from mutalyzer")
    return fetch_exons(transcript)


@app.route("/", methods=["GET"])
def index() -> str:
    # Put the default config into the session
    for key in config:
        if key not in session:
            session[key] = config[key]
    # Set DMD as default
    if "transcript" not in session:
        session["transcript"] = "NM_004006.3"

    return render_template("index.html")


def _update_config(config: Dict[str, Any], session: Any) -> Dict[str, Any]:
    """Update the configuration with values from the session"""
    d = config.copy()
    for key in d:
        d[key] = session[key]
    return d


@app.route("/", methods=["POST"])
def index_post() -> str:
    session["transcript"] = request.form["transcript"]
    session["height"] = int(request.form["height"])
    session["gap"] = int(request.form["gap"])
    session["noncoding"] = "noncoding" in request.form

    # Checkboxes only show up when set to true
    session["color"] = request.form["color"] or config["color"]

    session["width"] = int(request.form["width"])

    try:
        exons, reverse = cache_fetch(session["transcript"])
        session["svg"] = str(
            draw_exons(exons, reverse, config=_update_config(config, session))
        )
    except Exception as e:
        flash(str(e))
    return render_template("index.html")


@app.route("/draw/<transcript>", methods=["GET"])
def draw(transcript: str) -> str:
    exons, reverse = cache_fetch(transcript)
    return str(draw_exons(exons, reverse, config))


if __name__ == "__main__":
    app.secret_key = "super secret key"
    app.run()
