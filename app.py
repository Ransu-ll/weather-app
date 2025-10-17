from flask import Flask, render_template
import logging
from pathlib import Path
from flask import request, redirect, url_for , jsonify

ICON_MAP = {
    "Sunny": "weather-symbol-1-svgrepo-com.svg",
    "Cloudy": "weather-svgrepo-com (1).svg",
    "Rainy": "weather-rain-svgrepo-com.svg",
    "Mist": "weather-symbol-7-svgrepo-com.svg",
    "Windy": "weather-windy-svgrepo-com.svg",
    "Thunder": "weather-2-svgrepo-com.svg",
    "Night": "weather-color-moon-stars-svgrepo-com.svg",
    "Foggy": "weather-symbol-22-svgrepo-com.svg",
    "Default": "weather-svgrepo-com.svg"
}

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
    return render_template("index.jinja2")


# TODO: when user presses "go", it should redirect the user to the relevant town page containing 
# the town information

@app.route("/town/<town_url>")
def town_info(town_url):
    condition = "Cloudy"

    weather_data = {
        "town": town_url.replace("-", " ").title(),
        "date": "21.04.2025",
        "current_temp": 20,
        "condition": condition,
        "icon": ICON_MAP.get(condition, ICON_MAP["Default"]),
        "wind_speed": 6.1,
        "humidity": 90,
        "greeting": "Morning",
        "time": "12:27 PM",
        "forecast": [
            {"day": "Mon", "temp": 32, "condition": "Sunny"},
            {"day": "Tue", "temp": 12, "condition": "Rainy"},
            {"day": "Wed", "temp": 13, "condition": "Cloudy"},
            {"day": "Thu", "temp": 22, "condition": "Mist"},
            {"day": "Fri", "temp": 25, "condition": "Windy"},
            {"day": "Sat", "temp": 24, "condition": "Thunder"},
        ],
        "hourly": [
            {"time": "1 PM", "temp": 20, "condition": "Cloudy"},
            {"time": "2 PM", "temp": 21, "condition": "Rainy"},
            {"time": "3 PM", "temp": 21, "condition": "Rainy"},
            {"time": "4 PM", "temp": 20, "condition": "Cloudy"},
            {"time": "5 PM", "temp": 21, "condition": "Sunny"},
            {"time": "6 PM", "temp": 21, "condition": "Mist"},
        ]
    }

    # Add icon paths for each forecast and hourly entry
    for f in weather_data["forecast"]:
        f["icon"] = ICON_MAP.get(f["condition"], ICON_MAP["Default"])
    for h in weather_data["hourly"]:
        h["icon"] = ICON_MAP.get(h["condition"], ICON_MAP["Default"])

    return render_template("town.jinja2", weather=weather_data)



@app.route("/weather", methods=["GET"])
def weather_search():
    town = request.args.get("town")
    if town:
        formatted_town = town.lower().replace(", ", "-").replace(" ", "-")
        return redirect(url_for("town_info", town_url=formatted_town))
    return redirect(url_for("index"))
@app.route("/api/towns")
def api_towns():
    """Return list of towns from towns.txt as JSON for autocomplete."""
    town_list = list(towns_info.keys())
    return jsonify(town_list)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("notfound.jinja2", towns=list(towns_info.keys()))

