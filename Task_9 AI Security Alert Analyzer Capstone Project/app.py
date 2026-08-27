"""
app.py

Flask backend for the AI Security Alert Analyzer.

Responsibilities:
  - Serve the frontend (GET /)
  - Accept a raw security alert from the frontend (POST /api/analyze)
  - Validate the input
  - Send the alert to the OpenAI API using the system prompt defined in
    prompts.py
  - Parse and validate the structured JSON returned by the model
  - Return a clean JSON response to the frontend, or a helpful error
"""

import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI, OpenAIError

from prompts import SYSTEM_PROMPT

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

load_dotenv()  # Loads variables from a local .env file into the environment

app = Flask(__name__)

# Basic configuration
MAX_ALERT_LENGTH = 4000  # Maximum number of characters accepted from the user
MIN_ALERT_LENGTH = 10    # Minimum number of characters required to analyze
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

API_KEY = os.getenv("OPENAI_API_KEY")

# We only create the client if a key is present. If it's missing, requests
# to /api/analyze will fail gracefully with a clear error message instead of
# crashing the whole application on startup.
client = OpenAI(api_key=API_KEY) if API_KEY else None

# Fields that MUST be present in the AI's structured response.
REQUIRED_FIELDS = [
    "severity",
    "threat_type",
    "summary",
    "indicators",
    "recommended_actions",
    "confidence",
]

VALID_SEVERITIES = {"Low", "Medium", "High", "Critical"}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def validate_alert_input(alert_text):
    """
    Validates the raw alert text submitted by the user.

    Returns a tuple: (is_valid: bool, error_message: str or None)
    """
    if alert_text is None:
        return False, "Missing 'alert' field in request body."

    if not isinstance(alert_text, str):
        return False, "'alert' must be a string."

    stripped = alert_text.strip()

    if len(stripped) == 0:
        return False, "Alert text cannot be empty."

    if len(stripped) < MIN_ALERT_LENGTH:
        return False, (
            f"Alert text is too short to analyze. "
            f"Please provide at least {MIN_ALERT_LENGTH} characters."
        )

    if len(stripped) > MAX_ALERT_LENGTH:
        return False, (
            f"Alert text is too long. "
            f"Please limit input to {MAX_ALERT_LENGTH} characters."
        )

    return True, None


def validate_ai_response(data):
    """
    Validates that the parsed JSON returned by the AI contains all required
    fields with reasonable types/values. Raises ValueError if invalid.
    """
    if not isinstance(data, dict):
        raise ValueError("AI response is not a JSON object.")

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(f"AI response is missing fields: {', '.join(missing)}")

    if data["severity"] not in VALID_SEVERITIES:
        raise ValueError(f"Invalid severity value: {data['severity']}")

    if not isinstance(data["indicators"], list):
        raise ValueError("'indicators' must be a list.")

    if not isinstance(data["recommended_actions"], list):
        raise ValueError("'recommended_actions' must be a list.")

    try:
        confidence = int(data["confidence"])
    except (ValueError, TypeError):
        raise ValueError("'confidence' must be a number.")

    if confidence < 0 or confidence > 100:
        raise ValueError("'confidence' must be between 0 and 100.")

    # Normalize confidence back to an int in case it arrived as a float/string
    data["confidence"] = confidence

    return data


def analyze_alert_with_ai(alert_text):
    """
    Sends the alert text to the OpenAI API and returns the parsed,
    validated structured analysis as a Python dict.

    Raises RuntimeError for any failure (API error, bad JSON, schema
    mismatch) with a human-readable message suitable for the frontend.
    """
    if client is None:
        raise RuntimeError(
            "The server is not configured with an OpenAI API key. "
            "Set OPENAI_API_KEY in your .env file."
        )

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": alert_text},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
    except OpenAIError as exc:
        raise RuntimeError(f"OpenAI API error: {exc}") from exc

    raw_content = response.choices[0].message.content

    try:
        parsed = json.loads(raw_content)
    except (json.JSONDecodeError, TypeError) as exc:
        raise RuntimeError(
            "The AI returned a response that could not be parsed as JSON."
        ) from exc

    try:
        validated = validate_ai_response(parsed)
    except ValueError as exc:
        raise RuntimeError(f"The AI response failed validation: {exc}") from exc

    return validated


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serves the main frontend page."""
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    """
    Accepts a JSON body: {"alert": "<security alert text>"}
    Returns: {"success": true, "analysis": {...}} on success
             {"success": false, "error": "<message>"} on failure
    """
    body = request.get_json(silent=True)

    if body is None:
        return jsonify({
            "success": False,
            "error": "Request body must be valid JSON with an 'alert' field."
        }), 400

    alert_text = body.get("alert")

    is_valid, error_message = validate_alert_input(alert_text)
    if not is_valid:
        return jsonify({"success": False, "error": error_message}), 400

    try:
        analysis = analyze_alert_with_ai(alert_text.strip())
    except RuntimeError as exc:
        return jsonify({"success": False, "error": str(exc)}), 502

    return jsonify({"success": True, "analysis": analysis}), 200


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"success": False, "error": "Not found."}), 404


@app.errorhandler(500)
def server_error(_error):
    return jsonify({"success": False, "error": "Internal server error."}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # debug=True is convenient for local development; turn this off in
    # any real deployment.
    app.run(debug=True, port=5000)
