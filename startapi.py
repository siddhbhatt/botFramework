import subprocess
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

@app.route("/adminapi/botstart", methods=["POST"])
def interact_actions():
    data = request.get_json(force=True)
    botName = data['botName'] 
    s = subprocess.call(["python", "botstart.py", botName])
    #s = subprocess.Popen(["python", "botstart.py", "AdminBot"])
    print(s)
    return make_response(jsonify("Successful"), 200)

app.run(port=2030, debug=True)
