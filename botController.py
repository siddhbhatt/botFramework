from flask import Flask, request, jsonify
from coreFramework import Journey

app = Flask(__name__)
jm = Journey()

@app.route('/api/botController/', methods=['POST'])
def journeyManager():
    data = request.get_json(force=True)

    response = jm.executeJourney(data)
            
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=2000)