#import libraries
import json
import requests
import uuid
import time
import pandas as pd
import re

#Path variables
SESSION_PATH = 'config/session.json'
SESVARIABLE_PATH = 'config/sessionVariables.json'
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
    try:
        sesVariables = json.load(open(SESVARIABLE_PATH))
    except Exception as e:
        sesVariables = []
    
    def __init__(self):
        self.session = metadata.session
        self.sesVariables = metadata.sesVariables

    def saveSession(self):
        # saves session list into disk
        with open(self.sessionpath, "w") as outfile:
            json.dump(self.session, outfile)

    def deleteSession(self, sessionId):
        self.session = [i for i in self.session if not (i['sessionId'] == sessionId)]
        self.sesVariables = [i for i in self.sesVariables if not (i['sessionId'] == sessionId)]

    def upsertSesVariables(self, inputDict):
        match = 0
        for n in self.sesVariables:
            if isinstance(n, dict) and n['sessionId'] == inputDict['sessionId']:
                n['sessionVariables'] = n['sessionVariables'] + inputDict['sessionVariables']
                n['journeyName'] = inputDict['journeyName']
                n['blockName'] = inputDict['blockName']
                match = 1

        if match == 0:
            self.sesVariables.append(inputDict)

        print("debug line from upsertSesVariables - sesVariables = ", self.sesVariables)

    def querySesVariables(self, varList, sessionId, journeyName):
        ret = []
        for a in varList:
            for b in self.sesVariables:
                if b['sessionId'] == sessionId:
                    for c in b['sessionVariables']:
                        if a in c.keys():
                            if (c['scope'] == 'local' and b['journeyName'] == journeyName) or c['scope'] == 'global':
                                x = {a: c[a]}
                                ret.append(x)
        
        return ret
    

#Block class
class block(metadata):
    def __init__(self):
        self.session = super().session
        self.botdata = super().botdata
        self.intentendpoint = super().intentendpoint


    def getMsg(self):
        #receive and parse the input message
        pass

    def getVariables(self, journeyName, blockName, sessionId):
        getVariable=None
        #print("debug line from getVariables - i am here and sessionId = ", sessionId)
        for a in self.botdata['journey']:
            if a['journeyName'] == journeyName:
                for b in a['blocks']:
                    if b['blockName'] == blockName:
                        getVariable=b['getVariables']
                        #print("debug line from getVariables - getVariable = ", getVariable)
        
        if getVariable:
            res = self.querySesVariables(getVariable, sessionId, journeyName)
            print("debug line from getVariables - res = ", res)
            return res
        else:
            return []

    def getInput(self, journeyName, blockName, msg):
        for a in self.botdata['journey']:
            if a['journeyName'] == journeyName:
                for b in a['blocks']:
                    if b['blockName'] == blockName:
                        if b['type'] == 'input':
                            map = b['inputMapping']
                        else:
                            return []

        if len(map)>0:
            out = self.mapping(map, msg)
            print("debug line from getInput - out = ", out)
            return out
        else:
            return []

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

    def mapping(self, map, inp):
        out=[]
        
        for xmap in map:
            for key,value in xmap.items():
                if key == 'map':
                    for k, v in value.items():
                        lt = []
                        if k == 'path':
                            x = pd.json_normalize(inp, v).to_dict()
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
    
    def resolveVariables(self, inp, lookup, symbol):
        if isinstance(inp, list) and inp:
            out =[]
            for n in inp:
                #print ("Debug line - n = ", n)
                match = re.search(symbol + '(.*)' + symbol, str(n))
                if match and lookup:
                    for a in lookup:
                        if isinstance(a,dict):
                            for k,v in a.items():
                                if k == match.group(1):
                                    if isinstance(v,list):
                                        out = out + v
                                    else:
                                        out.append(v)
        elif isinstance(inp, str):
            out = inp
            matches = re.findall(symbol + '(.+?)' + symbol, out)
            if matches and lookup:
                for p in matches:
                    for q in lookup:
                        if p in q.keys():
                            new = q[p]
                            old = symbol + p + symbol
                            out = out.replace(old, new)

        return out

    def sendReponse(self, journeyName, blockName, api, inp, var):
        #response = {}
        for p in self.botdata['journey']:
            if p['journeyName'] == journeyName:
                for q in p['blocks']:
                    if q['blockName'] == blockName:
                        response = q['output']

        #print ("debug line - response = ", response)
        for i in response['message']['attachments']:
            #print("debug line - i = ", i)
            if i['options'] and api:
                x = self.resolveVariables(i['options'], api, '@')
                if x:
                    i['options'] = x

        a = self.resolveVariables(response['message']['messageText'], api, '@')
        b = self.resolveVariables(a, inp, '#')
        c = self.resolveVariables(b, var, '%')
        response['message']['messageText'] = c
        
        return response

    def setVariables(self, journeyName, blockName, sessionId, userId, inp):
        for p in self.botdata['journey']:
            if p['journeyName'] == journeyName:
                for q in p['blocks']:
                    if q['blockName'] == blockName:
                        if len(q['setVariables']) > 0:
                            vlist = q['setVariables']
                        else:
                            return
        
        svs = []
        for a in vlist:
            for key, val in a.items():
                if key == 'value':
                    rvalue = self.resolveVariables(val, inp, '#')
                    sv = {a['variableName']: rvalue, 'scope': a['scope']}
                    svs.append(sv)
        updDict = {'sessionId': sessionId, 'userId': userId, 'journeyName': journeyName, 
        'blockName': blockName, 'sessionVariables': svs}
        print("debug line from setVariables - updDict = ", updDict)
        self.upsertSesVariables(updDict)

        return

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

    def executeBlock(self, block, msg, **kwargs):
        if 'sessionId' in kwargs:
            var = self.getVariables(block['journeyName'], block['blockName'], kwargs['sessionId'])
        else:
            var = []
        mappedInput = self.getInput(block['journeyName'], block['blockName'], msg)
        check = self.applyRules()
        if check:
            mappedResponse = self.callAPI(block['journeyName'], block['blockName'])
            if 'sessionId' in kwargs:
                self.setVariables(block['journeyName'], block['blockName'], kwargs['sessionId'], kwargs['userId'], mappedInput)
            result = self.sendReponse(block['journeyName'], block['blockName'], mappedResponse, mappedInput, var)
            return result
