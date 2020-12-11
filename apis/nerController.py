import spacy
from flask import Flask, request, jsonify
import sys
import json

app = Flask(__name__)
botname = sys.argv[1]
BOTCONFIG_PATH = 'bots/'+botname+'/config/'+botname+'.json'
botdata = json.load(open(BOTCONFIG_PATH))
MODEL_PATH = 'bots/'+botname+'/models/ner'

@app.route('/api/nerController/', methods=['POST'])
def nerPredict():
    msg = request.get_json(force=True)
    nlp = spacy.load(MODEL_PATH)

    doc = nlp(msg)

    out=[]
    for ent in doc.ents:
        l = {ent.label_: ent.text}
        out.append(l)

    print ("out = ", out)

    return jsonify(out)

if __name__ == '__main__':
    #app.run(debug = True,port = 2006)
    nerControllerPort = botdata['deploy']['nerControllerPort']
    app.run(debug = True,port = int(nerControllerPort))
