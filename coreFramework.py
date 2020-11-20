#import libraries
import json
import requests
import uuid
import time
import pandas as pd
import re

#Path variables
SESSION_PATH = 'config/session.json'
BOTCONFIG_PATH = 'config/bot_booking.json'
INTENT_ENDPOINT = "http://127.0.0.1:2005/api/intentController/"

#Metadata class
class metadata:
    intentendpoint = INTENT_ENDPOINT
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
        """
        getVariable=None
        for getVar in self.botdata['journey']:
            for xgetVar in getVar['blocks']:
                if getVar.get('journeyName') == journeyName and xgetVar.get('blockSeq') == blockSeq:
                    getVariable=xgetVar.get('getVariables')
        return getVariable
        """
        pass

    def mapInput(self):
        pass

    def applyRules(self):
        """
        applyRules=None
        for getVar in self.botdata['journey']:
            for xgetVar in getVar['blocks']:
                if getVar.get('journeyName') == journeyName and xgetVar.get('blockSeq') == blockSeq:
                    applyRules=xgetVar.get('rules')
        print(InputMsg,applyRules)
        if InputMsg is not None:
            if InputMsg not in applyRules['message']:
                return False
            else:
                return True    
        else:
            return True
        """
        return True

    def callAPI(self, journeyName, blockName, **kwargs):
        for a in self.botdata['journey']:
            if a['journeyName'] == journeyName:
                for b in a['blocks']:
                    if b['blockName'] == blockName:
                        api = b.get('api')
        
        exStr = None
        output = None
        payload ={}
        if api['apiType'] == 'GET':
            if len(api['params']) > 0:
                for n in api['params']:
                    p = {n['key']: n['value']}
                    if not payload:
                        payload = p
                    else:
                        payload = payload.update(p)
                
            exStr = 'block.foo = lambda self: requests.get(url="' + str(api['endpoint']) + '", params=' + json.dumps(payload) +')'
            
        elif api['apiType'] == 'POST':
            payload = api['dataMapping']
            exStr = 'block.foo = lambda self: requests.post(url="' + str(api['endpoint']) + '", data=' + json.dumps(payload) +')'
        else:
            return []
            
        print ("exStr = ", exStr)
        
        try:
            exec(exStr)
            ex = self.foo()
            response = json.loads(ex.text)
            #print("debug line - response = ", response)
            if len(api['outputMapping']) > 0:
                output = self.mapping(api['outputMapping'], response)
                #print("debug line - output = ", output)
            else:
                output = response
        except Exception as e:
            print("Error from callAPI: ", e)
        return output

    def iterdict(self, d, lt):
        for k,v in d.items():
            if isinstance(v, dict):
                _ = self.iterdict(v, lt)
            else:
                lt.append(v)
        return lt

    def mapping(self, map, input):
        out=[]
        
        for xmap in map:
            for key,value in xmap.items():
                if key == 'map':
                    for k, v in value.items():
                        lt = []
                        if k == 'path':
                            x = pd.json_normalize(input, v).to_dict()
                            r = self.iterdict(x, lt)
                            if value['outputFormat'] == 'item' and len(r)==1:
                                d = {value['name']: r[0]}
                            elif value['outputFormat'] == 'arrayitem':
                                d = {value['name']: r}
                            elif value['outputFormat'] == 'jsonarray' and 'outputTag' in value.keys():
                                int_l = []
                                for n in r:
                                    int_d = {value['outputTag']: n}
                                    int_l.append(int_d)
                                d = {value['name']: int_l}
                            else:
                                print("Error from mapping: Invalid mapping")
                            out.append(d)

        return out

    def fixDtype(self, l):
        fixedList =[]
        for n in l:
            fixedList.append(json.loads(n))
        return fixedList
    
    def resolveVariables(self, x, response):
        if isinstance(x, list) and x:
            out =[]
            for n in x:
                #print ("Debug line - n = ", n)
                from_api = re.search('\@(.*)\@', str(n))
                if from_api:
                    for a in response:
                        if isinstance(a,dict):
                            for k,v in a.items():
                                if k == from_api.group(1):
                                    if isinstance(v,list):
                                        out = out + v
                                    else:
                                        out.append(v)

        return out

    def sendReponse(self, journeyName, blockName, r):
        #response = {}
        for p in self.botdata['journey']:
            if p['journeyName'] == journeyName:
                for q in p['blocks']:
                    if q['blockName'] == blockName:
                        response = q['output']

        #print ("debug line - response = ", response)
        for i in response['message']['attachments']:
            #print("debug line - i = ", i)
            if i['options'] and r:
                x = self.resolveVariables(i['options'], r)
                if x:
                    i['options'] = x

        
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
        self.getVariables()
        self.mapInput()
        check = self.applyRules()
        if check:
            response = self.callAPI(block['journeyName'], block['blockName'])
            self.setVariables()
            result = self.sendReponse(block['journeyName'], block['blockName'], response)
            return result
