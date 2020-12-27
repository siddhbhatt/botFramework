from flask import Flask, request, render_template,redirect, url_for
from flask import Response
#import pagebuild
import webbrowser
import json
app=Flask(__name__)
global univaljson
@app.route('/',methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('index.html')
    return render_template('bot_booking.html', error=error)
@app.route('/submit', methods=['POST'])
def submit():
    fnl=[]
    IntentsJ=''
    IntentsP=''
    i=0
    for x,y in request.form.items():
        if x[:x.find('[')] == 'IntentsP' and i==0:
            IntentsP=y
            i=1
        elif x[:x.find('[')] == 'IntentsJ' and i==1:
            IntentsJ=y
            i=0
        if IntentsP != '' and IntentsJ != '':
            fnl.append({'patterns':IntentsP,'journeyName':IntentsJ})
            IntentsP = ''
            IntentsJ =''
        json_conv=json.dumps({'intents':fnl})
        univaljson=json_conv
    return render_template('main.html',univaljson=univaljson,botname=request.form['botname'])
@app.route('/submitfinal', methods=['POST'])
def submitfinal():
    fnl=[]
    NREEntries=''
    NRE=''
    j=0
    #print(request.form['intents'])
    ##print('i m here :',request.form['NRE[0][]'])
    #print('game here:',request.form.items())
    for g in  request.form.items():
        #print('gg',g)
        #print('ggggg',g[0])
        f=g[0]
        if f[:f.find('[')] == 'NRE' and j==0:
            #print('help me')
            NRE=g[1]
            j=1
        elif f[:f.find('[')] == 'NREEntries' and j==1:
            NREEntries=g[1]
            j=0
        if NRE != '' and NREEntries != '':
            fnl.append({'patterns':NRE,'entities':NREEntries})
            NRE = ''
            NREEntries =''
    print('bbbbb>>>>',fnl,type(fnl))        
    json_conv2={'ner':fnl}
    json1=json.loads(request.form['intents'])
    json_conv2.update(json1)
    json_conv2.update({'botName':request.form['botname']})
    json_conv2=json.dumps(json_conv2)
    print('************',json_conv2)
    #return render_template('main.html')
    return render_template('dynamic.html',univaljson=json_conv2,botname=request.form['botname'])
@app.route('/workflowfinal', methods=['POST'])
def workflowfinal():
    fndlst=[]
    blkdictlst={}
    blkdictlstinput={}
    blkdictlstapi={}
    blkdictlstapidataMapping={}
    blkdictlstapidataMappingmap={}
    blkdictlstapidataoutput={}
    blkdictlstnext={}
    blkdictlstsetvar={}
    blkdictlstgetvar={}
    blkdictlstrules={}
    blkdictlstbase={}
    fnllistdict={}
    for f in request.form:
        #f=x[0]
        print('f-->',request.form.get(f),'~',f)
        if f[:f.find('[')] == 'jrn':
            
            fndlst.append({'journeyName':request.form.get(f)})
            print('fndlst>',fndlst)
        elif f[:f.find('[')] == 'list':
            blkdictlst['blockName']=request.form.get(f)
            #blkdictlstbase.append(blkdict)
        elif f[:f.find('[')] == 'blktype':
            blkdictlst['type']=request.form.get(f)
        elif f[:f.find('[')] == 'getvariable':
            blkdictlst['getVariables']=request.form.get(f)
        elif f[:f.find('[')] == 'rule':
            blkdictlstrules['oneOf']=request.form.get(f)
        elif f[:f.find('[')] == 'imdata':
            blkdictlstinput['name']=request.form.get(f)
        elif f[:f.find('[')] == 'imchannel':
            blkdictlstinput['path']=request.form.get(f)
            print('blkdictlstinput1>',blkdictlstinput)
        elif f[:f.find('[')] == 'imuser':
            blkdictlstinput['outputFormat']=request.form.get(f)
            print('blkdictlstinput2>',blkdictlstinput)
        #API CALL COMMING#
        
        
        elif f[:f.find('[')] == 'apiurl':
            blkdictlstapi['endpoint']=request.form.get(f)
            print('blkdictlstapi>',blkdictlstapi)
        elif f[:f.find('[')] == 'apitype':
            blkdictlstapi['apiType']=request.form.get(f)
            print('blkdictlstapi1>',blkdictlstapi)
        elif f[:f.find('[')] == 'apiparams':
            blkdictlstapi['params']=request.form.get(f)
            
        elif f[:f.find('[')] == 'apidmbotname':
            blkdictlstapidataMapping['botName']=request.form.get(f)
        elif f[:f.find('[')] == 'apidmoptiontext':
            blkdictlstapidataMapping['optionText']=request.form.get(f)
        
        elif f[:f.find('[')] == 'apidmname':
            blkdictlstapidataMappingmap['name']=request.form.get(f)
        elif f[:f.find('[')] == 'apidmpath':
            blkdictlstapidataMappingmap['path']=request.form.get(f)
        elif f[:f.find('[')] == 'apidmoutformat':
            blkdictlstapidataMappingmap['outputFormat']=request.form.get(f)
        elif f[:f.find('[')] == 'apidmoutputtag':
            blkdictlstapidataMappingmap['outputTag']=request.form.get(f)
        #output changes
        elif f[:f.find('[')] == 'outmessageId':
            blkdictlstapidataoutput['messageId']=request.form.get(f)
        elif f[:f.find('[')] == 'outmessageText':
            blkdictlstapidataoutput['messageText']=request.form.get(f)
        elif f[:f.find('[')] == 'outmessageType':
            blkdictlstapidataoutput['messageType']=request.form.get(f)
        elif f[:f.find('[')] == 'outattachment':
            blkdictlstapidataoutput['attachments']=request.form.get(f)
        #Next Variables#
        elif f[:f.find('[')] == 'njourneyName':
            blkdictlstnext['journeyName']=request.form.get(f)
        elif f[:f.find('[')] == 'nblockName':
            blkdictlstnext['blockName']=request.form.get(f)
        #Set Variables#
        elif f[:f.find('[')] == 'svariableName':
            blkdictlstsetvar['variableName']=request.form.get(f)
        elif f[:f.find('[')] == 'svalue':
            blkdictlstsetvar['value']=request.form.get(f)
        elif f[:f.find('[')] == 'sscope':
            blkdictlstsetvar['scope']=request.form.get(f)
        #Get Variables#
        elif f[:f.find('[')] == 'variableName':
            blkdictlstgetvar['variableName']=request.form.get(f)
        elif f[:f.find('[')] == 'value':
            blkdictlstgetvar['value']=request.form.get(f)
        elif f[:f.find('[')] == 'scope':
            blkdictlstgetvar['scope']=request.form.get(f)
            
    blkdictlstapidataoutput={'message':blkdictlstapidataoutput}
    #blkdictlstapidataoutput={'output':blkdictlstapidataoutput}
    #blkdictlstrules={'rules':blkdictlstrules}
    #blkdictlstnext={'next':[blkdictlstnext]}
    #blkdictlstsetvar={'setVariables':[blkdictlstsetvar]}
    #blkdictlstgetvar={'getVariables':[blkdictlstgetvar]}
    blkdictlstapidataMappingmap={'map':blkdictlstapidataMappingmap}
    #blkdictlstapidataMapping={'dataMapping':blkdictlstapidataMapping}
    blkdictlstapi['dataMapping']=blkdictlstapidataMapping
    blkdictlstapi['outputMapping']=[blkdictlstapidataMappingmap]
    #apidict={'api':blkdictlstapi}
    #inputMappingdict={'inputMapping':{'map':blkdictlstinput}}
    apidict=[]
    inputMappingdict=[]
    fnllist=[blkdictlst,apidict,inputMappingdict]
    blkdictlst.update(blkdictlstbase)
    blkdictlst['blockSeq']=1
    blkdictlst['next']=[blkdictlstnext]
    blkdictlst['setVariables']=[blkdictlstsetvar]
    blkdictlst['getVariables']=[blkdictlstgetvar]
    blkdictlst['rules']=blkdictlstrules
    blkdictlst['inputMapping']={'map':blkdictlstinput}
    blkdictlst['api']=blkdictlstapi
    blkdictlst['output']=blkdictlstapidataoutput
    fnllistdict={'blocks':[blkdictlst]}
    json1=json.loads(request.form['intents'])
    fnllistdict.update(json1)
    fnllistdict.update({'botName':request.form['botname']})
    json_conv2=json.dumps(fnllistdict)
    return render_template('deploy.html',univaljson=json_conv2,botname=request.form['botname'])
    #return Response(json_conv2,headers={'Content-Disposition':'attachment;filename=model.json'})
    #return json_conv2
@app.route('/deploy', methods=['POST'])
def deploy():
    deploydict={}
    deploydict['channel']=request.form['channel']
    deploydict['botControllerPort']=request.form['botControllerPort']
    deploydict['intentControllerPort']=request.form['intentControllerPort']
    deploydict['nerControllerPort']=request.form['nerControllerPort']
    deploydict['slackInteractPort']=request.form['slackInteractPort']
    deploydict['slackSendMessagePort']=request.form['slackSendMessagePort']
    deploydict['slackAppName']=request.form['slackAppName']
    deploydict['slackBotToken']=request.form['slackBotToken']
    deploydict['slackVerToken']=request.form['slackVerToken']
    fnldict={'deploy':deploydict}
    json1=json.loads(request.form['intents'])
    fnldict.update(json1)
    fnldict.update({'botName':request.form['botname']})
    json_conv2=json.dumps(fnldict)
    return json_conv2
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 4040)