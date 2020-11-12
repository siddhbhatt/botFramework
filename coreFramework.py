#import libraries
import json
import requests
import uuid
import time

#Path variables
SESSION_PATH = 'config/session.json'
BOTCONFIG_PATH = 'config/bot_booking.json'
INTENT_ENDPOINT = "http://127.0.0.1:2005/api/intentController/"

#Metadata class
class metadata:
    intentendpoint = INTENT_ENDPOINT
    #intents = json.loads(open("../config/bot_booking.json"))
    botdata = json.load(open(BOTCONFIG_PATH))
    try:
        session = json.load(open(SESSION_PATH))
    except Exception as e:
        session = []
    
    def __init__(self):
        self.session = metadata.session

    def saveSession(self):
        # saves session list into disk
        with open(self.sessionpath, "w") as outfile:
            json.dump(self.session, outfile)

    def deleteSession(self, sessionId):
        self.session = [i for i in self.session if not (i['sessionId'] == sessionId)]

#Block class
class block(metadata):
    def __init__(self):
        self.session = super().session
        self.botdata = super().botdata
        self.intentendpoint = super().intentendpoint


    def getMsg(self):
        #receive and parse the input message
        pass

    def getVariables(self):
        pass

    def applyRules(self):
        pass

    def callApi(self):
        pass

    def mapOutput(self):
        pass

    def sendReponse(self, journeyName, blockName):
        response = {}
        for p in self.botdata['journey']:
            if p['journeyName'] == journeyName:
                for q in p['blocks']:
                    if q['blockName'] == blockName:
                        response = q['output']
        return response

    def setVariables(self):
        pass

    def getNext(self, journeyName, **kwargs):
        next = []
        for x in self.botdata['journey']:
            if x['journeyName'] == journeyName:
                for y in x['blocks']:
                    if 'blockName' in kwargs:
                        if y['blockName'] == kwargs['blockName']:
                            next = y['next']
                            print ("next >>", next)
                    else:
                        if y['blockSeq'] == 1:
                            next = [{'journeyName': x['journeyName'], 'blockName': y['blockName']}]
        return next


class sessionManager(block):
    def __init__(self):
        self.session = super().session
        self.botdata = super().botdata
        self.intentendpoint = super().intentendpoint
        
    def getSession(self, user):
        #return sessionId, JourneyName, blockName
        currSession = {}
        for i in self.session:
            if i['userId'] == user:
                currSession = i
        return currSession
    
    def createSession(self, user, journeyName, blockName, blockSeq):
        sessionId = str(uuid.uuid1())
        startTS = time.time()
        self.session.append({'sessionId': sessionId, 'userId': user, 
        'journeyName': journeyName, 'blockName': blockName, 'blockSeq': blockSeq,
        'startTS': startTS})
        return sessionId, startTS

    def updateSession(self, user, journeyName, blockName, blockSeq):
        startTS = time.time()
        for i in self.session:
            if i['userId'] == user:
                sessionId = i['sessionId']
                i.update({'journeyName': journeyName, 'blockName': blockName, 'blockSeq': blockSeq,
                'startTS': startTS})
        return sessionId, startTS

    def getIntent(self, message, **kwargs):
        intent={}
        try:
            r = requests.post(url=self.intentendpoint, data=json.dumps(message))
            intent = json.loads(r.text)
        except Exception as e:
            print(e)
        return intent

    def executeBlock(self, block):
        response = self.sendReponse(block['journeyName'], block['blockName'])
        return response

