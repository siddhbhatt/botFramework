from subprocess import Popen, PIPE
import os
import json
import sys

botName = sys.argv[1]
deployConfig = json.load(open('bots/'+botName+'/config/'+botName+'.json'))
logpath = 'logs/'+botName+'/'
if not os.path.exists('logs/'+botName):
    os.makedirs('logs/'+botName)

processes = [
    [['python', 'botController.py', botName],'botController.log'],
    [['python', 'apis/intentController.py', botName], 'intentController.log']
]

if deployConfig['ner']:
    #print("enableNER=", deployConfig['deploy']['enableNER'])
    nerprocess = [['python', 'apis/nerController.py', botName], 'nerController.log']
    processes.append(nerprocess)

if deployConfig['deploy']['channel'] == 'Slack':
    slackprocesses = [[['python', 'channelAdapters/slack/sendmessage.py', botName], 'sendmessage.log'], 
        [['python', 'channelAdapters/slack/interact.py', botName], 'interact.log'],
        [['python', 'channelAdapters/slack/rtmclient.py', botName], 'rtmclient.log']]
    processes = processes + slackprocesses
    #print("slack=", processes)
elif deployConfig['deploy']['channel'] == 'TKinter':
    tkprocess = [['python', 'channelAdapters/tkinter/tkinteract.py', botName], 'tkinteract.log']
    processes.append(tkprocess)

print("processes = ", processes)

for n in processes:
    with open (logpath+n[1], 'w') as logfile:
        logfile.flush()
        plist = [Popen(n[0], stdout=logfile, stderr=logfile)]

try:
    for proc in plist:
        proc.wait()
except KeyboardInterrupt:
    for proc in plist:
        try:
            proc.terminate()
        except OSError as e:
            print(e)
        proc.wait()