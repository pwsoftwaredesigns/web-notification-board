from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import argparse 

PORT = 5000
TIMESTAMP_FORMAT = "%A, %B %m %I:%M:%S %p"
MAX_MESSAGES = 100

app = Flask(__name__)
CORS(app)

message_history = []

@app.route('/')
def index():
    arg_clock = request.args.get('clock', 'false').lower() == 'true'
    arg_edit = request.args.get('edit', 'false').lower() == 'true'
    arg_n = int(request.args.get('n', 3))
    arg_name = request.args.get('name', 'Anonymous')
    arg_refresh = int(request.args.get('refresh', 3000))
    arg_osk = request.args.get('osk', 'false').lower() == 'true'
    
    return render_template('viewer.html', arg_clock=arg_clock, arg_edit=arg_edit, arg_n=arg_n, arg_name=arg_name, arg_refresh=arg_refresh, arg_osk=arg_osk)

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
    reply_text = data.get('message')
    reply_name = data.get('name', 'Anonymous')

    if message_id >= len(message_history) or message_id < 0:
        return jsonify({'status': 'Invalid message ID'}), 400
        	
    if not reply_text:
    	return jsonify({'status': 'Message is required'}), 400

    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    reply_data = {
        'name': reply_name,
        'message': reply_text,
        'timestamp': timestamp
    }
    
    message_history[message_id]['replies'].insert(0, reply_data)
    return jsonify({'status': 'Reply added successfully!'})

@app.route('/clear', methods=['POST'])
def clear_messages():
    global message_history
    message_history = []
    return jsonify({'status': 'All messages cleared successfully!'})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Flask server for the web notification board")
    parser.add_argument("--debug", action="store_true", help="Enable debugging mode")
    args = parser.parse_args()
	
    if args.debug:
	    #Enable autoamtic template reloading so that ap does not need to be restarted
	    app.config['TEMPLATES_AUTO_RELOAD'] = True
	
    app.run(host='0.0.0.0', port=PORT)
