from flask import Flask
from loguru import logger

from .main import document_blueprint

logger.debug("Starting Server")
app = Flask(__name__)

url_prefix = "/api/v1"

logger.debug("Loading Blueprints")
app.register_blueprint(document_blueprint, url_prefix=url_prefix)

if __name__ == "__main__":
    app.run()
