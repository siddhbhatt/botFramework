import tkinter
from tkinter import *
import uuid
import requests
import json

USER_ID = str(uuid.uuid1())
BOT_ENDPOINT = "http://127.0.0.1:2000/api/botController/"

def prep_response(msg):
    data = {'user': USER_ID,
    'message': {'messageId':str(uuid.uuid1()), 'messageText': msg, 'messageType': 'plaintext',
    'attachments': []}}
    r = requests.post(url = BOT_ENDPOINT, data = json.dumps(data))
    json_out =  json.loads(r.text)
    print ("botController response >> ", json_out)
    responses = []
    for i in json_out:
        if 'message' in i.keys():
            responses.append(i['message']['messageText'])
    return responses


def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
    
        responses = prep_response(msg)
        if responses:
            for res in responses:
                ChatLog.insert(END, "TestBot2: " + res + '\n\n')
                    
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
 

base = Tk()
base.title("Tk.TestBot2")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

base.mainloop()