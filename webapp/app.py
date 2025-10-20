from flask import Flask, render_template, request
import logging
from pathlib import Path
from bidict import bidict

from .LocationInfoDownloader import retreive_town_info

logger = logging.getLogger(__name__)

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
    towns_info[town] = sanitise_str(town.lower().replace(", ", "-").replace(" ", "-"))

@app.route("/")
def index():
    logger.info("Connected to index")
    return render_template("index.jinja2", towns=towns_info)

# TODO: when user presses "go", it should redirect the user to the relevant town page containing 
# the town information
# 1. user looks up a town 
# 2. most relevant towns by name are shown, if any
# 3. user selects a town
# 4. server checks if it has a file downloaded from the town
# 4.1.0. server does not have town
# 4.1.1. server downloads town information
# 4.2.0. server has town
# 4.2.1. server must check datetime that file was downloaded
# 4.2.2. if greater than 10 minutes, download new file, else keep current data
# 5. pass the data to the template

@app.route("/town/<town_url>")
def town_info(town_url):
    town_url = sanitise_str(town_url)
    if town_url not in towns_info.values():
        logger.warning(f"Could not find {town_url}")
        return render_template("notfound.jinja2", towns=towns_info)
    logger.info(f"Connected to {town_url}")

    current_town = towns_info.inverse[town_url]
    # Town data should get the latest forecast of the town data
    town_data = retreive_town_info(current_town)
    logger.info(town_data)

    return render_template("town.jinja2", towns=towns_info, town_data=town_data, town_name=current_town)

@app.route("/town_info_get", methods=["GET"])
def town_info_get():
    current_town = request.args["town"]
    current_town = sanitise_str(current_town)
    logger.info(current_town)

    if current_town not in towns_info.keys():
        logger.warning(f"Could not find {current_town}")
        return render_template("notfound.jinja2", towns=towns_info)
    logger.info(f"Requested for {current_town}")

    # Town data should get the latest forecast of the town data
    town_data = retreive_town_info(current_town)

    return render_template("town.jinja2", towns=towns_info, town_data=town_data, town_name=current_town)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.jinja2", towns=towns_info)