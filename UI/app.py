from flask import Flask, request, render_template,redirect, url_for
from flask import Response
#import pagebuild
import webbrowser
import json
app=Flask(__name__)
global univaljson
@app.route('/')
def index():
    return render_template('index.html')
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
    i=0
    print(request.form['intents'])
    for x,y in request.form.items():
        print('c>>',x,y)
        if x[:x.find('[')] == 'NRE' and i==0:
            NRE=y
            i=1
        elif x[:x.find('[')] == 'NREEntries' and i==1:
            NREEntries=y
            i=0
        if NRE != '' and NREEntries != '':
            fnl.append({'patterns':NRE,'entities':NREEntries})
            NRE = ''
            NREEntries =''


        json_conv=json.dumps({'ner':fnl})
        print(json_conv)
        json1=dict(request.form['intents'])
        val2=request.form['botname']
        json_conv.update(json1)
    #return render_template('main.html')
    return Response(json_conv,headers={'Content-Disposition':'attachment;filename=model.json'})
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 4040)