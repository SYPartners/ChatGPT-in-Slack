#!/usr/bin/env python3
"""
Render deployment wrapper that provides:
1. Health check endpoint for Render
2. Blocks all other HTTP requests
3. Runs Socket Mode Slack app
"""
import os
import threading
import logging
from flask import Flask, make_response, request

# Create Flask app for health checks only
health_app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@health_app.route("/healthz", methods=["GET"])
def health_check():
    """Health check endpoint for Render - matches express-wrapper.js pattern"""
    return make_response("OK", 200)

@health_app.route("/", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@health_app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def block_all_other_requests(path=None):
    """Block all other HTTP requests for security"""
    logger.warning(f"Blocked request: {request.method} {request.path} from {request.remote_addr}")
    return make_response("Forbidden", 403)

def run_slack_app():
    """Run the Slack Socket Mode app in a separate thread"""
    logger.info("Starting Slack Socket Mode app...")
    # Import and run main.py directly
    import subprocess
    subprocess.run(["python", "main.py"])

if __name__ == "__main__":
    # Start Slack app in a separate thread
    slack_thread = threading.Thread(target=run_slack_app, daemon=True)
    slack_thread.start()
    logger.info("Slack app thread started")
    
    # Run Flask app for health checks on Render's port
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting health check server on port {port}")
    health_app.run(host="0.0.0.0", port=port)