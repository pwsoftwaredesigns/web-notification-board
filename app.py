from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

PORT = 5000
TIMESTAMP_FORMAT = "%A, %B %m %I:%M:%S %p"
MAX_MESSAGES = 100


app = Flask(__name__)
CORS(app)

# Updated message history to hold a list of dictionaries
message_history = []

@app.route('/')
def index():
    return render_template('viewer.html')

@app.route('/sender')
def sender():
    return render_template('sender.html')

@app.route('/display', methods=['GET', 'POST'])
def display_messages():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name', 'Anonymous')
        message = data.get('message')

        if not message:
            return jsonify({'status': 'Message is required'}), 400

        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
        message_id = len(message_history)
        message_history.append({'id': message_id, 'name': name, 'message': message, 'timestamp': timestamp, 'replies': []})

        if len(message_history) > MAX_MESSAGES:
            message_history.pop(0)

        return jsonify({'status': 'Message received successfully!'})

    elif request.method == 'GET':
        n = request.args.get('N', default=1, type=int)
        n = max(1, min(n, len(message_history)))

        return jsonify({'messages': message_history[-n:]})

@app.route('/reply', methods=['POST'])
def add_reply():
    data = request.get_json()
    message_id = data.get('messageId')
    reply = data.get('reply')

    if message_id >= len(message_history) or message_id < 0:
        return jsonify({'status': 'Invalid message ID'}), 400

    message_history[message_id]['replies'].insert(0, reply)
    return jsonify({'status': 'Reply added successfully!'})

@app.route('/clear', methods=['POST'])
def clear_messages():
    global message_history
    message_history = []
    return jsonify({'status': 'All messages cleared successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
    