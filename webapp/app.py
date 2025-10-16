from flask import Flask
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def index():
    logger.info("Connected to index")
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    logger.info("Connected to test")
    return "<p>Test!</p>"