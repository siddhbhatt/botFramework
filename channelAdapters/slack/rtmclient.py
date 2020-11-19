from slack import RTMClient
from slack.errors import SlackApiError
import requests
import json
import uuid

SLACK_BOT_TOKEN = 'xoxb-1464215873904-1448607286740-I6aOkhGmybOhBpJyh7z1bGtD'
BOT_ENDPOINT = "http://127.0.0.1:2000/api/botController/"
SEND_ENDPOINT = "http://127.0.0.1:2015/slack/sendMessage/"

def send_message(msg, channel):
    pdata = {'message': msg, 'channel': channel}
    r1 = requests.post(url =SEND_ENDPOINT, data = json.dumps(pdata))
    response1 =  json.loads(r1.text)
    print ("sendMessage response >> ", response1)

def invokeBot(user, msg, channel):
    data = {'user': user, 'message': {'messageId': str(uuid.uuid1()), 'messageText': msg, 'messageType': 'text', 'attachments':[]}}
    r = requests.post(url = BOT_ENDPOINT, data = json.dumps(data))
    response =  json.loads(r.text)
    print ("botController response >> ", response)
    
    for res in response:
        if 'message' in res:
            send_message(res['message'], channel)


@RTMClient.run_on(event='message')
def read_msg(**payload):
    print(payload)
    
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'username' in data.keys():
        username = data['username']
    else:
        username = ''
    if 'text' in data and username != 'TestBot2':
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        msg = data['text']
        
        invokeBot(user, msg, channel_id)
        

rtm_client = RTMClient(token=SLACK_BOT_TOKEN)
rtm_client.start()