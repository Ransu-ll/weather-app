from waitress import serve
from webapp.app import app
import logging, os

logging.basicConfig(level=logging.INFO)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

if __name__ == "__main__":
    serve(app, host=HOST, port=PORT)