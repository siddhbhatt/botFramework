import spacy
from flask import Flask, request, jsonify

app = Flask(__name__)
MODEL_PATH = 'models/ner/model'

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
    app.run(debug = True,port = 2006)
