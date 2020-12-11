from flask import Flask, request, jsonify, make_response
from slack import WebClient
import json
import requests
import sys

# Set parameters, tokens and variables
botname = sys.argv[1]
botdata = json.load(open('bots/'+botname+'/config/'+botname+'.json'))
SLACK_BOT_TOKEN = botdata['deploy']['slackBotToken']
SLACK_VERIFICATION_TOKEN = botdata['deploy']['slackVerToken']
BOT_ENDPOINT = 'http://127.0.0.1:#port#/api/botController/'.replace('#port#', botdata['deploy']['botControllerPort'])
SEND_ENDPOINT = "http://127.0.0.1:#port#/slack/sendMessage/".replace('#port#', botdata['deploy']['slackSendMessagePort'])


# Slack client for Web API requests
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# Flask webserver for incoming traffic from Slack
app = Flask(__name__)

# Helper for verifying that requests came from Slack
def verify_slack_token(request_token):
    if SLACK_VERIFICATION_TOKEN != request_token:
        print("Error: invalid verification token!")
        print("Received {} but was expecting {}".format(request_token, SLACK_VERIFICATION_TOKEN))
        return make_response("Request contains invalid Slack verification token", 403)

def translate_message(j):
    if j['type'] == 'block_actions':
        user = j['user']['id']
        channel = j['channel']['id']
        messageId = j['message']['blocks'][0]['block_id']
        messageText = j['message']['blocks'][0]['text']['text']
        messageType = 'plaintext'
        attachments = []

        seq = 1
        for n in j['message']['blocks']:
            if n['type'] == 'section' and 'accessory' in n.keys() and n['accessory']['type'] in ['static_select', 'datepicker', 'checkboxes']:
                options = []
                optionSelected = []
                attachmentId = n['accessory']['action_id']
                attachmentSeq = seq
                attachmentDesc = n['text']['text']
                if n['accessory']['type'] == 'static_select':
                    attachmentType = 'dropdown'
                    optionSelected.append({'value': j['state']['values'][messageId][attachmentId]['selected_option']['value']})
                elif n['accessory']['type'] == 'datepicker':
                    attachmentType = 'datepicker'
                    optionSelected.append({'value': j['state']['values'][messageId][attachmentId]['selected_date']})
                elif n['accessory']['type'] == 'checkboxes':
                    attachmentType = 'checkbox'
                if n['accessory']['type'] != 'datepicker':
                    for o in n['accessory']['options']:
                        opt = {'value': o['value']}
                        options.append(opt)
                
                atc = {'attachmentId': attachmentId, 'attachmentSeq': attachmentSeq, 'attachmentDesc': attachmentDesc,
                'attachmentType': attachmentType, 'options': options, 'optionsSelected': optionSelected
                }
                attachments.append(atc)
                seq = seq+1
            elif n['type'] == 'actions':
                attachmentId = n['block_id']
                attachmentSeq = seq
                attachmentDesc = ''
                attachmentType = 'button'
                options = []
                for o in n['elements']:
                    if o['type'] == 'button':
                        e = {'value':o['value']}
                        options.append(e)
                optionSelected = []
                for s in j['actions']:
                    if s['block_id'] == attachmentId:
                        t = {'value':s['value']}
                        optionSelected.append(t)
                atc = {'attachmentId': attachmentId, 'attachmentSeq': attachmentSeq, 'attachmentDesc': attachmentDesc,
                'attachmentType': attachmentType, 'options': options, 'optionsSelected': optionSelected
                }
                attachments.append(atc)
                seq = seq + 1

        msg = {'user':user, 'message': {
            'messageId': messageId, 'messageText': messageText, 'messageType': messageType,
            'attachments':attachments
        }}

        return msg, channel

def send_message(msg, channel):
    pdata = {'message': msg, 'channel': channel}
    r1 = requests.post(url =SEND_ENDPOINT, data = json.dumps(pdata))
    response1 =  json.loads(r1.text)
    print ("sendMessage response >> ", response1)
    return

def invoke_bot(msg, channel):
    r = requests.post(url = BOT_ENDPOINT, data = json.dumps(msg))
    response =  json.loads(r.text)
    print ("botController response >> ", response)
    
        
    for res in response:
        if res and 'message' in res:
            send_message(res['message'], channel)
    return

@app.route("/slack/interact", methods=["POST"])
def interact_actions():  
    # Parse the request payload
    form_json = json.loads(request.form["payload"])
    print("debug line - form_json = ", form_json)

    # Verify that the request came from Slack
    verify_slack_token(form_json["token"])

    tmsg, channel = translate_message(form_json)
    print("debug line - tmsg = ", tmsg)

    bot_response = invoke_bot(tmsg, channel)

    return make_response("", 200)

#app.run(debug=True, port=2025)
app.run(debug=True, port=int(botdata['deploy']['slackInteractPort']))