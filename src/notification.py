import logging
import os
from flask import Flask, request, jsonify, abort

app = Flask(__name__)


@app.route("/", methods=["POST"])
def receive_data():
    # Check if JSON data is provided
    if not request.is_json:
        logging.error(f"Missing JSON in request: {request}")
        abort(400, "Missing JSON in request")

    data: dict = request.get_json()  # parse json data from the request
    process_data(data)  # get data from json and print it

    return jsonify({"message": "Received data successfully"}), 200


def process_data(data: dict):
    client_id = data.get("client_id")
    user_id = data.get("user_id")
    event_type = data.get("event_type")
    timestamp = data.get("timestamp")
    severity = data.get("severity")
    correlation_id = data.get("correlation_id")

    log_message = (
        f"Received data! - "
        f"Client ID: {client_id} - "
        f"User ID: {user_id} - "
        f"Event Type: {event_type} - "
        f"Timestamp: {timestamp} - "
        f"Severity: {severity} - "
        f"Correlation ID: {correlation_id}"
    )
    logging.info(log_message)


if __name__ == "__main__":
    # Enable debug mode in development environment
    if os.environ.get("FLASK_ENV") == "development":
        app.debug = True
    logging.basicConfig(level=logging.INFO)
    app.run(port=5000)
