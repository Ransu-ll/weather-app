from waitress import serve
import app

# Specify the logging level for app.py
app.logging.basicConfig(level=app.logging.INFO)

serve(app.app, listen="127.24.58.10:1224")