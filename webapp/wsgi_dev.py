# from waitress import serve
# from app import app
# import logging, os

# logging.basicConfig(level=logging.INFO)

# HOST = os.getenv("HOST", "0.0.0.0")
# PORT = int(os.getenv("PORT", "8000"))

# if __name__ == "__main__":
#     serve(app, host=HOST, port=PORT)

from waitress import serve
import app

# Specify the logging level for app.py
app.logging.basicConfig(level=app.logging.INFO)

serve(app.app, listen="127.24.58.10:1224")