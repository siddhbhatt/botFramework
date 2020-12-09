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
    j=0
    print(request.form['intents'])
    print('i m here :',request.form['NRE[0][]'])
    print('game here:',request.form.items())
    for g in  request.form.items():
        print('gg',g)
        print('ggggg',g[0])
        f=g[0]
        if f[:f.find('[')] == 'NRE' and j==0:
            print('help me')
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
    return Response(json_conv2,headers={'Content-Disposition':'attachment;filename=model.json'})
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 4040)
