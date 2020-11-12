from flask import Flask, request, jsonify
from slack import WebClient

# Your app's Slack bot user token
SLACK_BOT_TOKEN = 'xoxb-1464215873904-1448607286740-I6aOkhGmybOhBpJyh7z1bGtD'

# Slack client for Web API requests
web_client = WebClient(token=SLACK_BOT_TOKEN)
app = Flask(__name__)

def prep_section(msg):
    sc = [
        {'type': 'section', 'text': {'type': 'mrkdwn', 'text': msg}}
    ]
    return sc

def post_section(section, channel):
    try:
        response = web_client.chat_postMessage(
            channel=channel,
            blocks=section)
        return response
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

@app.route('/slack/sendMessage/', methods=['POST'])
def send_message():
    data = request.get_json(force=True)

    section = prep_section(data['message'])
    _ = post_section(section, data['channel'])
    return jsonify(section)

if __name__ == '__main__':
    app.run(debug=True, port=2015)