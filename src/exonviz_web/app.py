from flask import (
    Blueprint,
    Flask,
    Response,
    render_template,
    session,
    request,
    flash,
    url_for,
)
from typing import Tuple, List, Dict, Any
import secrets
import functools

from exonviz import draw_exons, config, Exon
from exonviz import mutalyzer
from exonviz.cli import check_input, get_MANE

# Set up flask
app = Flask(__name__)
bp = Blueprint("exonviz", __name__)
app.register_blueprint(bp)

# Pull FLASK_SECRET_KEY from environment, or use fallback random ID
app.config.from_prefixed_env()
if not app.config.get("SECRET_KEY"):
    app.secret_key = secrets.token_hex()

# Log the secret key
app.logger.info(f"Secret key: {app.config['SECRET_KEY']}")


MANE = get_MANE()


@functools.cache
def cache_fetch_exons(transcript: str) -> Dict[str, Any]:
    """Wrapper to cache calls to mutalyzer"""
    app.logger.info(f"Fetching {transcript} from mutalyzer")
    return mutalyzer.fetch_exons(transcript)


@functools.cache
def cache_fetch_variants(transcript: str) -> Dict[str, Any]:
    """Wrapper to cache calls to mutalyzer"""
    app.logger.info(f"Fetching variants for {transcript} from mutalyzer")
    return mutalyzer.fetch_variants(transcript)


def build_exons(transcript: str, config: Dict[str, Any]) -> List[Exon]:
    exons = cache_fetch_exons(transcript)
    variants = cache_fetch_variants(transcript)
    return mutalyzer.build_exons(transcript, exons, variants, config)


@app.route("/", methods=["GET"])
def index() -> str:
    # Put the default config into the session
    for key in config:
        if key not in session:
            session[key] = config[key]
    # Set DMD as default
    if "transcript" not in session:
        session["transcript"] = "NM_003002.4:r.[274G>T;300del]"
    # Set the width as default
    session["width"] = 1024
    # Set the first and last exon
    session["firstexon"] = 1
    session["lastexon"] = 1000

    return render_template("index.html")


def _update_config(config: Dict[str, Any], session: Any) -> Dict[str, Any]:
    """Update the configuration with values from the session"""
    d = config.copy()
    for key in d:
        d[key] = session[key]
    return d


def rewrite_transcript(transcript: str, MANE: Dict[str, str]) -> str:
    """Rewrite the transcript, if needed"""
    if transcript in MANE:
        transcript = MANE[transcript]
    return check_input(transcript)


@app.route("/", methods=["POST"])
def index_post() -> str:
    session["transcript"] = request.form["transcript"]
    session["height"] = int(request.form["height"])
    session["scale"] = float(request.form["scale"])
    session["gap"] = int(request.form["gap"])
    session["firstexon"] = int(request.form["firstexon"])
    session["lastexon"] = int(request.form["lastexon"])
    session["noncoding"] = "noncoding" in request.form
    session["exonnumber"] = "exonnumber" in request.form

    # Checkboxes only show up when set to true
    session["color"] = request.form["color"] or config["color"]

    session["width"] = int(request.form["width"])

    download_url = url_for("draw", **session)

    try:
        # Rewrite the transcript
        session["transcript"] = rewrite_transcript(session["transcript"], MANE)
        exons = build_exons(
            session["transcript"], config=_update_config(config, session)
        )
        figure = str(draw_exons(exons, config=_update_config(config, session)))
    except Exception as e:
        flash(str(e))
        figure = ""
    return render_template("index.html", figure=str(figure), download_url=download_url)


@app.route("/draw", methods=["GET"])
def draw() -> Response:
    figure_config: dict[str, Any] = dict(request.args)

    # Cast integer values to int
    for field in ["firstexon", "lastexon", "gap", "height", "width"]:
        figure_config[field] = int(figure_config[field])

    # Cast boolean values to boolean
    for field in ["exonnumber", "noncoding"]:
        figure_config[field] = figure_config[field] == "True"

    # Pull out the transcript name
    transcript = figure_config.pop("transcript")

    exons = build_exons(transcript, figure_config)
    figure = str(draw_exons(exons, figure_config))

    return Response(
        figure,
        mimetype="text/svg",
        headers={"Content-disposition": f"attachment; filename={transcript}.svg"},
    )
