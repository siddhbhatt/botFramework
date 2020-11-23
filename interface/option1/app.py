#Arghadeep_____Bot4Bot@22-11-2020 
from flask import Flask, request, render_template,redirect, url_for
from flask import Response
import pagebuild
import json
app=Flask(__name__)
data_path=r'C:\Users\ArghadeepChaudhury\Downloads\botFramework-main\botFramework-main\config\bot_booking.json'
bot_data=json.load(open(data_path))
pb=pagebuild.pageBuild
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/submit', methods=['POST'])
def submit():
    datareturn=[]
    cdata=''
    ValField=''
    getVariables=''
    inputMapping=''
    if request.form.get("action")=='Load Template':
        for xintent in bot_data.get('intents'):
            if xintent.get('journeyName') == request.form['db']:
                datareturn.append(xintent.get('patterns'))
        for xxdata in bot_data.get('journey'):
            if xxdata.get('journeyName') == request.form['db']:#type
                for xxxdata in xxdata.get('blocks'):
                    inputMapping='<b><u>inputMapping</b></u><br/>'+pb.field(str(xxxdata.get('inputMapping').get('data')),'data',str(xxxdata.get('blockSeq')))+pb.field(str(xxxdata.get('inputMapping').get('channel')),'channel',str(xxxdata.get('blockSeq')))+pb.field(str(xxxdata.get('inputMapping').get('user')),'user',str(xxxdata.get('blockSeq')))
                    ValField='<div style="border-style: solid;border-color: coral;">'+ValField+pb.field(xxxdata.get('blockName'),'BlockName',str(xxxdata.get('blockSeq')))+pb.dropdown('BlockType','BlockType',str(xxxdata.get('type')),'input','output')+'<br/>'+pb.textarea(str(xxxdata.get('getVariables')),'Get Variables: ')+'</br>'+pb.textarea(str(xxxdata.get('rules')),'Set Rules: ')+inputMapping+'<br/><br/></div>'
    for xdatareturn in datareturn:
        cdata=cdata+'\n'+str(xdatareturn)
    intrn=pb.textarea(cdata,'Intent Pattern: ')
    intrn=pb.HTMLTextHead+intrn+ValField+pb.HTMLTextTail
    return intrn
if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 4001)