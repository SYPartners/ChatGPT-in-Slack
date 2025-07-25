#!/usr/bin/env python3
"""
Wrapper for running the Slack app on Render with health check support.
This runs the Socket Mode app while also providing an HTTP endpoint for health checks.
"""
import os
import threading
from flask import Flask, make_response
from main import app, SocketModeHandler

# Create Flask app for health check
health_app = Flask(__name__)

@health_app.route("/slack/events", methods=["GET", "POST"])
def health_check():
    """Health check endpoint for Render"""
    return make_response("OK", 200)

@health_app.route("/", methods=["GET"])
def root():
    """Root endpoint"""
    return make_response("Slack app is running", 200)

def run_slack_app():
    """Run the Slack Socket Mode app in a separate thread"""
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

if __name__ == "__main__":
    # Start Slack app in a separate thread
    slack_thread = threading.Thread(target=run_slack_app, daemon=True)
    slack_thread.start()
    
    # Run Flask app for health checks on port 10000 (Render's default)
    port = int(os.environ.get("PORT", 10000))
    health_app.run(host="0.0.0.0", port=port)