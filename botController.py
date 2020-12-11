from flask import Flask, request, jsonify
from coreFramework import Journey
import sys
import json

app = Flask(__name__)
botname = sys.argv[1]
jm = Journey(botname)

@app.route('/api/botController/', methods=['POST'])
def journeyManager():
    data = request.get_json(force=True)

    response = jm.executeJourney(data)
            
    return jsonify(response)


if __name__ == '__main__':
    botdata = json.load(open('bots/'+botname+'/config/'+botname+'.json'))
    botControllerPort = botdata['deploy']['botControllerPort']
    app.run(debug=True, port=int(botControllerPort))