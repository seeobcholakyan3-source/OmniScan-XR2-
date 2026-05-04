from flask import Flask
from flask_cors import CORS
from api.routes import routes
from core.logger import get_logger

app = Flask(__name__)
CORS(app)

logger = get_logger("OmniOrchestrator")

app.register_blueprint(routes)

if __name__ == "__main__":
    logger.info("Starting OmniScan-XR2 v2 backend...")
    app.run(host="0.0.0.0", port=5001)
