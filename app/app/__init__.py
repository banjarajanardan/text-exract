from flask import Flask
from flask_cors import CORS
from loguru import logger

from .main import document_blueprint
from .main.services.google_service import init_google_vision

logger.debug("Starting Server")
app = Flask(__name__)
CORS(app)

url_prefix = "/api/v1"

logger.debug("Checking Google Credentials")
init_google_vision()

logger.debug("Loading Blueprints")
app.register_blueprint(document_blueprint, url_prefix=url_prefix)

if __name__ == "__main__":
    app.run()
