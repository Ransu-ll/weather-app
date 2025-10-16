from flask import Flask, render_template
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

app = Flask(__name__)

location_this_file = Path(__file__).parent.resolve()

towns = location_this_file / "static/towns.txt"

with open(towns, "r") as f:
    towns = f.read()

towns = towns.split("\n")
print(towns[0])


@app.route("/")
def index():
    logger.info("Connected to index")
    return render_template("index.jinja2", towns=towns)

@app.route("/test")
def test():
    logger.info("Connected to test")
    return "<p>Test!</p>"