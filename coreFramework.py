#import libraries
import json
import requests
import uuid
import time
import pandas as pd
import re

#Path variables
#SESSION_PATH = 'config/session.json'
#SESVARIABLE_PATH = 'config/sessionVariables.json'
#BOTCONFIG_PATH = 'config/adminbot.json'
INTENT_ENDPOINT = "http://127.0.0.1:#port#/api/intentController/"
NER_ENDPOINT = 'http://127.0.0.1:#port#/api/nerController/'

#Session class
class Session:
    """
    try:
        session = json.load(open(SESSION_PATH))
    except OSError:
        session = []
    try:
        sesVariables = json.load(open(SESVARIABLE_PATH))
    except OSError:
        sesVariables = []
    """
    
    def __init__(self, botname):
        self.botname = botname
        try:
            self.session = json.load(open('bots/'+self.botname+'/config/session.json'))
            self.sesVariables = json.load(open('bots/'+self.botname+'/config/sessionVariables.json'))
        except OSError:
            self.session =[]
            self.sesVariables = []

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

    def saveSession(self):
        # saves session list into disk
        with open(self.sessionpath, "w") as outfile:
            json.dump(self.session, outfile)

    def deleteSession(self, user):
        self.session = [i for i in self.session if not (i['userId'] == user)]
        self.sesVariables = [i for i in self.sesVariables if not (i['userId'] == user)]
        print("debug line from deleteSession - session = ", self.session)
        print("debug line from deleteSession - sesVariables = ", self.sesVariables)

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
class Block(Session):
    #botdata = json.load(open(BOTCONFIG_PATH))
    
    def __init__(self, botname):
        super(Block, self).__init__(botname=botname)
        self.botdata = json.load(open('bots/'+self.botname+'/config/'+self.botname+'.json'))
        if self.botdata['ner']:
            self.nerEndpoint = NER_ENDPOINT.replace('#port#', self.botdata['deploy']['nerControllerPort'])

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
            x = [i for i in map if 'map' in i.keys()]
            y = [i for i in map if 'ner' in i.keys()]
            out1 = []
            out2 = []
            if x:
                out1 = self.mapping(x, msg)
            if y:
                out2 = self.nerMapping(y, msg)
            out = out1 + out2
            print("debug line from getInput - out = ", out)
            return out
        else:
            return []

    def applyRules(self, journeyName, blockName, inp, var):
        #print("debug line from applyRules - i am here")
        rules = {}
        check = True
        for a in self.botdata['journey']:
            if a['journeyName'] == journeyName:
                for b in a['blocks']:
                    if b['blockName'] == blockName and b['rules']:
                        rules = b['rules']
                        #print("debug line from applyRules - rules = ", rules)
        
        if rules:   
            for n in rules['oneOf']:
                for k, v in n.items():
                    inp_r = self.resolveVariables(k, inp, '#')
                    var_r = self.resolveVariables(inp_r, var, '%')
                    #print("debug line from applyRules - var_r = ", var_r, " v = ", v)
                    if var_r == v:
                        check = True
                    else:
                        check = False
                        break

                #print("debug line from applyRules - check = ", check)
                if check == True:
                    return check
 
        return check

    def callAPI(self, journeyName, blockName, var, inp):
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
                
            exStr = 'Block.foo = lambda self: requests.get(url="' + str(api['endpoint']) + '", params=' + json.dumps(payload) +')'
            
        elif api['apiType'] in ['POST', 'PUT']:
            payload_r1 = self.resolveVariables(api['dataMapping'], var, '%')
            payload_r2 = self.resolveVariables(payload_r1, inp, '#')
            exStr = 'Block.foo = lambda self: requests.' + api['apiType'].lower() + '(url="' + str(api['endpoint']) + '", json=' + json.dumps(payload_r2) +')'
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
                            if isinstance(v, list):
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
                            elif isinstance(v, str):
                                if value['outputFormat'] == 'item':
                                    d = {value['name']:inp[v]}
                            else:
                                print("Error from mapping: Invalid mapping")
                            out.append(d)

        return out

    def nerMapping(self, map, inp):
        out = []

        data = inp['messageText']
        r = requests.post(url=self.nerEndpoint, data=json.dumps(data))
        rjson = json.loads(r.text)
        
        for xmap in map:
            for k, v in xmap.items():
                for ent in rjson:
                    if v['entity'] in ent.keys() and v['outputFormat'] == 'item':
                        var = {v['name']: ent[v['entity']]}
                        out.append(var)
        print("debug line from nerMapping - out = ", out)
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
            #print("Debug line from resolveVariables - matches = ", matches)
            if matches and lookup:
                for p in matches:
                    for q in lookup:
                        if p in q.keys():
                            new = q[p]
                            old = symbol + p + symbol
                            out = out.replace(old, new)
        elif isinstance(inp, dict):
            out = inp
            for k, v in out.items():
                if isinstance(v, str):
                    match = re.search(symbol + '(.*)' + symbol, v)
                    if match and lookup:
                        for a in lookup:
                            for b, c in a.items():
                                if b == match.group(1):
                                    print ("Debug line from resolveVariables - b =", b, "\nmatch = ", c)
                                    out[k] = c
            print("Debug line from resolveVariables - out = ", out)

        return out

    def sendReponse(self, journeyName, blockName, api, inp, var):
        for p in self.botdata['journey']:
            if p['journeyName'] == journeyName:
                for q in p['blocks']:
                    if q['blockName'] == blockName:
                        output = q['output'].copy()

        #print ("debug line - response = ", response)
        for i in output['message']['attachments']:
            #print("debug line - i = ", i)
            if i['options'] and api:
                x = self.resolveVariables(i['options'], api, '@')
                if x:
                    i['options'] = x
        
        if output['message']['messageText']:
            a = self.resolveVariables(output['message']['messageText'], api, '@')
            b = self.resolveVariables(a, inp, '#')
            c = self.resolveVariables(b, var, '%')
            output['message']['messageText'] = c
        
        return output

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
                            #print ("next >>", next)
                    else:
                        if y['blockSeq'] == 1:
                            next = [{'journeyName': x['journeyName'], 'blockName': y['blockName']}]
        return next

    def executeBlock(self, block, msg, **kwargs):
        if 'sessionId' in kwargs:
            var = self.getVariables(block['journeyName'], block['blockName'], kwargs['sessionId'])
        else:
            var = []
        mappedInput = self.getInput(block['journeyName'], block['blockName'], msg)
        check = self.applyRules(block['journeyName'], block['blockName'], mappedInput, var)
        if check:
            mappedResponse = self.callAPI(block['journeyName'], block['blockName'], var, mappedInput)
            if 'sessionId' in kwargs:
                self.setVariables(block['journeyName'], block['blockName'], kwargs['sessionId'], kwargs['userId'], mappedInput)
            result = self.sendReponse(block['journeyName'], block['blockName'], mappedResponse, mappedInput, var)
            return result

class Journey(Block):
    def __init__(self, botname):
        super(Journey, self).__init__(botname=botname)
        self.intentendpoint = INTENT_ENDPOINT.replace('#port#', self.botdata['deploy']['intentControllerPort'])
        #self.nerEndpoint = NER_ENDPOINT
        #self.session = super().session
        #self.botdata = super().botdata
        
    def getIntent(self, message, **kwargs):
        intent={}
        try:
            r = requests.post(url=self.intentendpoint, data=json.dumps(message))
            intent = json.loads(r.text)
        except Exception as e:
            print("Error from getIntent - ", e)
        return intent

    def startNewJourney(self, msg, user):
        self.deleteSession(user)
        self.botdata = json.load(open('bots/'+self.botname+'/config/'+self.botname+'.json'))
        #self.botdata = json.load(open(BOTCONFIG_PATH))
        jny = self.getIntent(msg['messageText'])
        next = self.getNext(jny['intent'])
        n=0
        res = []
        for i in next:
            res.append(self.executeBlock(i, msg))
            if n==0:
                _, _ = self.createSession(user, i['journeyName'], i['blockName'], i['blockName'])
            else:
                _, _ = self.updateSession(user, i['journeyName'], i['blockName'], i['blockName'])
            n = n+1
        return res

    def executeJourney(self, data):
        response = []
        ses = self.getSession(data['user'])

        if 'sessionId' in ses:
            next = self.getNext(ses['journeyName'], blockName=ses['blockName'])
            if len(next) == 0:
                #self.deleteSession(ses['sessionId'])
                response = self.startNewJourney(data['message'], data['user'])
            else:
                for i in next:
                    response.append(self.executeBlock(i, data['message'], sessionId=ses['sessionId'], userId=ses['userId']))
                    _, _ = self.updateSession(ses['userId'], 
                    i['journeyName'], i['blockName'], i['blockName'])
        else:
            response = self.startNewJourney(data['message'], data['user'])

        return response