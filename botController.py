from flask import Flask, request, redirect, url_for, flash, jsonify
from coreFramework import sessionManager

app = Flask(__name__)
sm = sessionManager()

def startJourney(msg, user):
    journey = sm.getIntent(msg['messageText'])
    next = sm.getNext(journey['intent'])
    n=0
    res = []
    for i in next:
        res.append(sm.executeBlock(i, msg))
        if n==0:
            _, _ = sm.createSession(user, i['journeyName'], i['blockName'], i['blockName'])
        else:
            _, _ = sm.updateSession(user, i['journeyName'], i['blockName'], i['blockName'])
        n = n+1
    return res

@app.route('/api/botController/', methods=['POST'])
def journeyManager():
    data = request.get_json(force=True)

    session = sm.getSession(data['user'])
    response = []

    if 'sessionId' in session:
        next = sm.getNext(session['journeyName'], blockName=session['blockName'])
        if len(next) == 0:
            sm.deleteSession(session['sessionId'])
            response = startJourney(data['message'], data['user'])
        else:
            for i in next:
                print(i)
                response.append(sm.executeBlock(i, data['message'], sessionId=session['sessionId'], userId=session['userId']))
                _, _ = sm.updateSession(session['userId'], 
                i['journeyName'], i['blockName'], i['blockName']) #should update based on sessionId and item in next list
    else:
        response = startJourney(data['message'], data['user'])
            
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=2000)