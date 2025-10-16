from flask import Flask, render_template
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

app = Flask(__name__)

location_this_file = Path(__file__).parent.resolve()

towns = location_this_file / "static/towns.txt"

with open(towns, "r") as f:
    towns = f.read()


towns_info = {}

for town in towns.split("\n"):
    towns_info[town] = town.lower().replace(", ", "-").replace(" ", "-")

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

@app.route("/")
def index():
    logger.info("Connected to index")
    return render_template("index.jinja2", towns=towns_info)

# TODO: when user presses "go", it should redirect the user to the relevant town page containing 
# the town information

@app.route("/town/<town_url>")
def town_info(town_url):
    town_url = sanitise_str(town_url)
    if town_url not in town_info.keys():
        logger.warning(f"Could not find {town_url}")
        return render_template("notfound.jinja2", towns=list(towns_info.keys()))
    logger.info(f"Connected to {town_url}")
    return render_template("town.jinja2", towns=list(towns_info.keys()))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.jinja2", towns=list(towns_info.keys()))