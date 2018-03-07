from flask import Flask, request, current_app
from pprint import pprint
from inforsender import start_infosender, stop_infosender
from classinfocrawler import get_classinfo_in_coming_week, start_infocrawler, stop_infocrawler
from receivedmsgverifier import message_authentication
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "<p>Hello World!</p>"

@app.route('/callback', methods=['POST'])
def callback(*args, **argd):
    # Verify that the msg is from Line platform
    sig = request.headers.get('X-Line-Signature', '')
    # Get the request body
    body = request.get_data(as_text=True)

    verified_ok = message_authentication(body, sig)
    if not verified_ok:
        return ''

    json_line = request.get_json()
    if not json_line:
        return ''
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    pprint(decoded)
    evts = decoded.get('events', [])
    for evt in evts:
        msg = evt.get('message', '')
        msg_type = evt.get('type', '')
        source   = evt.get('source', {})
        user_type = source.get('type', '')
        user_id = source.get('userId', '') if user_type == 'user' else ''
        timestamp   = evt.get('timestamp', 0)
        reply_token = evt.get('replyToken', '')
        print("使用者： {}".format(user_id))
        print("內容： {}".format(msg))
        if msg.get('text', '') == '123':
            get_classinfo_in_coming_week()

    return ''

def start_app():
    start_infosender()
    start_infocrawler()
    app.run(debug=True, use_reloader=False)
    stop_infocrawler()
    stop_infosender()