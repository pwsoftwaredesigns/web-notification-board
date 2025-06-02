from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

PORT = 5000
TIMESTAMP_FORMAT = "%A, %B %m %I:%M:%S %p"
MAX_MESSAGES = 100


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store message history as a list of tuples (message, timestamp)
message_history = []

@app.route('/')
def index():
    return render_template('viewer.html')  # Serve the viewer page (or add a route for sender)

@app.route('/sender')
def sender():
    return render_template('sender.html')  # Serve the sender page


@app.route('/display', methods=['GET', 'POST'])
def display_messages():
    # Sender sends a message via POST
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', 'Anonymous')
        message = data.get('message')
        
        if not message:
            return jsonify({'status': 'Message is required'}), 400

        # Append message with its timestamp to history
        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)  # Get the current time as a string
        message_history.append((name, message, timestamp))
        
        # Optional: Limit message history to last 100 messages
        if len(message_history) > MAX_MESSAGES:
            message_history.pop(0)  # Remove the oldest message

        return jsonify({'status': 'Message received successfully!'})

    # Viewer requests last N messages via GET
    elif request.method == 'GET':
        # Extract "N" from the query parameters
        n = request.args.get('N', default=1, type=int)
        n = max(1, min(n, len(message_history)))  # Ensure N is within bounds

        # Format the result to include messages with timestamps
        messages_with_timestamps = [{'name': msg[0], 'message': msg[1], 'timestamp': msg[2]} for msg in message_history[-n:]]
        return jsonify({'messages': messages_with_timestamps})

@app.route('/clear', methods=['POST'])
def clear_messages():
    global message_history
    message_history = []  # Clear all stored messages
    return jsonify({'status': 'All messages cleared successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
    