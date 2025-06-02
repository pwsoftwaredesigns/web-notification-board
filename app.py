from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

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
        message = data.get('message', '')

        # Append message with its timestamp to history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current time as a string
        message_history.append((message, timestamp))
        
        # Optional: Limit message history to last 100 messages
        if len(message_history) > 100:
            message_history.pop(0)  # Remove the oldest message

        return jsonify({'status': 'Message received successfully!'})

    # Viewer requests last N messages via GET
    elif request.method == 'GET':
        # Extract "N" from the query parameters
        n = request.args.get('N', default=1, type=int)
        n = max(1, min(n, len(message_history)))  # Ensure N is within bounds

        # Format the result to include messages with timestamps
        messages_with_timestamps = [{'message': msg[0], 'timestamp': msg[1]} for msg in message_history[-n:]]
        return jsonify({'messages': messages_with_timestamps})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    