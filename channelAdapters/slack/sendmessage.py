from flask import Flask, request, jsonify
from slack import WebClient
from slack.errors import SlackApiError

# Your app's Slack bot user token
SLACK_BOT_TOKEN = 'xoxb-1464215873904-1448607286740-I6aOkhGmybOhBpJyh7z1bGtD'

# Slack client for Web API requests
web_client = WebClient(token=SLACK_BOT_TOKEN)
app = Flask(__name__)

def prep_accessory(attachment):
    accessory = None
    response_type = 'accessory'
    if attachment['attachmentType'] in ['dropdown', 'checkbox', 'datepicker']:
        if attachment['attachmentType'] == 'dropdown':
            slack_type = 'static_select'
        elif attachment['attachmentType'] == 'datepicker':
            slack_type = 'datepicker'
        else:
            slack_type = 'checkboxes'
        #response_type = 'accessory'
        
        accessory = {'action_id': attachment['attachmentId'], 'type': slack_type}
        
        options =[]
        initial_options =[]
        
        if 'options' in attachment.keys():
            for a in attachment['options']:
                opt = {'text': {'type': 'plain_text', 'text': a['value']},
                'value': a['value']}
                options.append(opt)
                if 'setInitial' in a.keys() and a['setInitial'] == True:
                    i_option = {'text': {'type': 'plain_text', 'text': a['value']},
                    'value': a['value']}
                    initial_options.append(i_option)
            
            if len(options) > 0:
                accessory['options'] = options
            
            if len(initial_options) > 0:
                accessory['initial_options'] = initial_options
    
    elif attachment['attachmentType'] == 'button':
        slack_type = response_type = 'actions'
        accessory = {'type': slack_type, 'block_id': attachment['attachmentId'],
        'elements': []}
        for a in attachment['options']:
            option = {'type': 'button','text': {'type': 'plain_text', 'text': a['value']}, 'value':  a['value']}
            accessory['elements'].append(option)
    
    return response_type, accessory

def prep_section(msg):
    if msg['messageType'] == 'plaintext':
        sc = [
            {'type': 'section', 'block_id': msg['messageId'], 
            'text': {'type': 'mrkdwn', 'text': msg['messageText']}}
        ]

    if 'attachments' in msg.keys():
        n=0
        for attachment in msg['attachments']:
            response_type, accessory = prep_accessory(attachment)
            if response_type == 'accessory':
                if n >= len(sc):
                    sc_new = {'type': 'section', 'block_id': attachment['attachmentId'], 
                    'text': {'type': 'mrkdwn', 'text': attachment['attachmentDesc']}}
                    sc.append(sc_new)
                if accessory:
                    sc[n]['accessory'] = accessory
            elif response_type == 'actions':
                if accessory:
                    sc.append(accessory)
            n = n+1
    
    print ("section >> ", sc)
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