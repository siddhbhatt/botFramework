from flask import Flask, request, jsonify, make_response
import json
import os
import subprocess

STARTER_JSON = 'config/starter.json'
app = Flask(__name__)

@app.route('/adminapi/botHeader/', methods=['POST', 'PUT'])
def postBotHeader():
    data = request.get_json(force=True)
    print("data = ", data)
    botName = data['botName']

    if not os.path.exists('bots/'+botName):
        os.makedirs('bots/'+botName+'/config')
        botdata = json.load(open(STARTER_JSON))
    else:
        botdata = json.load(open('bots/'+botName+'/config/'+botName+'.json'))

    for k1 in data.keys():
        for k2 in botdata.keys():
            if k2 == k1 and k1 != 'journey':
                botdata[k2] = data[k1]
    
    if 'optionText' in data.keys():
        for n in botdata['journey']:
            if n['journeyName'] == 'options':
                n['blocks'][0]['output']['message']['messageText'] = data['optionText']

    with open('bots/'+botName+'/config/'+botName+'.json',"w") as out:
        json.dump(botdata, out)

    return make_response(jsonify("Successful"), 200)

@app.route('/adminapi/journey/', methods=['POST'])
def postJourney():
    data = request.get_json(force=True)
    botName = data['botName']

    try:
        botdata = json.load(open('bots/'+botName+'/config/'+botName+'.json'))
    except OSError as e:
        print("Error from postJourney - ", e)
        return make_response("Illegal operation - botdata doesn't exist", 500)
    
    exst_jny = [a['journeyName'] for a in botdata['journey']]
    new_jny = [b['journeyName'] for b in data['journey']]

    check = any(item in exst_jny for item in new_jny)
    if check:
        return make_response("Illegal operation - journeyName already exists", 500)
    
    botdata['journey'] = botdata['journey'] + data['journey']

    with open('bots/'+botName+'/config/'+botName+'.json',"w") as out:
        json.dump(botdata, out)
    
    return make_response(jsonify("Successful"), 200)

def updateBotData(dct, jny, botdata):
    blk = [i for i in botdata['journey'] if i['journeyName']==jny]
    for n in blk[0]['blocks']:
        if n['blockName'] == dct['blockName']:
            n.update(dct)

    return botdata

@app.route('/adminapi/journey/', methods=['PUT'])
def putJourney():
    data = request.get_json(force=True)
    botName = data['botName']

    try:
        botdata = json.load(open('bots/'+botName+'/config/'+botName+'.json'))
    except OSError as e:
        print("Error from postJourney - ", e)
        return make_response("Illegal operation - botdata doesn't exist", 500)

    for i in data['journey']:
        for j in i['blocks']:
            updbotdata = updateBotData(j, i['journeyName'], botdata)

    with open('bots/'+botName+'/config/'+botName+'.json',"w") as out:
        json.dump(updbotdata, out)
    
    return make_response(jsonify("Successful"), 200)

@app.route('/adminapi/botdata/', methods=['GET'])
def getJourney():
    params = request.args.to_dict()
    print(params)
    botName = params['botName']

    try:
        botdata = json.load(open('bots/'+botName+'/config/'+botName+'.json'))
    except OSError as e:
        print("Error from postJourney - ", e)
        return make_response("Illegal operation - botdata doesn't exist", 500)

    return jsonify(botdata)

@app.route("/adminapi/botstart", methods=["POST"])
def interact_actions():
    data = request.get_json(force=True)
    botName = data['botName']
    proc = data['process']
    s = subprocess.call(["python", proc, botName])
    #s = subprocess.Popen(["python", "botstart.py", "AdminBot"])
    print(s)
    return make_response(jsonify("Successful"), 200)

app.run(port=2030, debug=True)