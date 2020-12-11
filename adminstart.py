from subprocess import Popen, PIPE
import os

logpath = 'C:/Users/SIDDHARTHABHATTACHAR/Documents/Copy/MachineLearning/sampleProjects/logbotFramework/'

"""
processes = [[['python', 'botController.py'], 'botController.log'],
[['python', './apis/intentController.py'], 'intentController.log'],
[['python', './apis/test/cities.py'], 'cities.log'],
[['python', './channelAdapters/slack/rtmclient.py'], 'rtmclient.log'],
[['python', './channelAdapters/slack/sendmessage.py'], 'sendmessage.log'],
[['python', './channelAdapters/slack/interact.py'], 'interact.log'],
[['python', './apis/nerController.py'], 'nerController.log'],
[['python', './channelAdapters/tkinter/tkinteract.py'], 'tkinteract.log']]
"""
processes = [[['python', './apis/intentController.py'], 'intentController.log'],
[['python', './apis/test/cities.py'], 'cities.log'],
[['python', './channelAdapters/slack/rtmclient.py'], 'rtmclient.log'],
[['python', './channelAdapters/slack/sendmessage.py'], 'sendmessage.log'],
[['python', './channelAdapters/slack/interact.py'], 'interact.log'],
[['python', './apis/nerController.py'], 'nerController.log']]


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

