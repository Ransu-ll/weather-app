from flask import Flask, render_template, request, redirect, abort
import logging
from pathlib import Path
from bidict import bidict
from datetime import datetime
import pprint


try:
    from webapp.LocationInfoDownloader import retreive_town_info
except Exception as e:
    from LocationInfoDownloader import retreive_town_info

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

location_this_file = Path(__file__).parent.resolve()

towns_file = location_this_file / "data/towns.txt"

with open(towns_file, "r") as f:
    towns = f.read()


def sanitise_str(to_sanitise):
    return to_sanitise.translate(str.maketrans({
    "-":  r"\-",
    "]":  r"\]",
    "\\": r"\\",
    "^":  r"\^",
    "$":  r"\$",
    "*":  r"\*",
    ".":  r"\."
}))

towns_info = bidict({})

for town in towns.split("\n"):
    towns_info[town] = town.lower().replace(", ", "-").replace(" ", "-")

@app.route("/")
def index():
    logger.info("Connected to index")
    return render_template("index.jinja2", towns=towns_info)

@app.route("/town/<town_url>")
def town_info(town_url):
    logger.info(f"Connected to {town_url}")

    try:
        current_town_url = towns_info.inverse[town_url]
    except KeyError:
        logger.warning(f"{request.remote_addr} tried to find town via direct link:\n{town_url}")
        return abort(400)
    
    # Town data should get the latest forecast of the town data
    town_data = retreive_town_info(current_town_url)
    logger.info(town_data)

    return render_template("town.jinja2",
                       towns=towns_info,
                       town_data=town_data,
                       town_name=current_town_url,
                       current_time=datetime.now())

@app.route("/town_info_get", methods=["GET"])
def town_info_get():
    current_town = request.args["town"]
    logger.info(f"Searched for {current_town} via GET method")

    try:
        current_town_url = towns_info[current_town]
    except KeyError:
        logger.warning(f"{request.remote_addr} tried to find following town name via GET:\n{current_town}")
        return abort(400)
    return redirect(f"town/{current_town_url}")


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/404")

@app.errorhandler(400)
def town_not_found(e):
    return redirect("/400")


@app.route("/404")
def _404():
    return render_template("notfound.jinja2", towns=towns_info, whatNotFound="page", prompt="Why not search for a town instead?")

@app.route("/400")
def _400():
    return render_template("notfound.jinja2", towns=towns_info, whatNotFound="town", prompt="Enter a valid town")