from waitress import serve
from webapp.app import app
import logging
import os

# Specify the logging level for app.py
logging.basicConfig(level=app.logging.INFO)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

serve(app.app, host=HOST, port=PORT)