from flask import Flask, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

@app.route('/testapi/cities')
def getCities():

    out = {
        "country": {
            "name": ["India"],
            "states": [
                {
                    "name": ["WB"],
                    "cities": ["Kolkata", "Burdwan"],
                    "county": [{"name": ["C1"], "id": 1}],
                    "ward": [{"city": "kolkata", "no": [132, 110, 144]}]
                },
                {
                    "name": ["AP"],
                    "cities": ["Hyderabad"],
                    "ward": [{"city": "Hyderabad", "no": [221, 32, 11]}],
                    "county": [{"name": ["C2"], "id": 4}]
                }
            ]
        },
        "continent": ["Asia"]
    }

    return jsonify(out)

app.run(port=2020, debug=True)