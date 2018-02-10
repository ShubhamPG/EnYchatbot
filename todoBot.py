import json 
import requests
import time 
#from urllib import quote_plus

TOKEN = "544315494:AAGQ7Oj4gKURC54F_6MdFjQoOW-gZgKNMsk"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

##----------------------    Remove and put this code into module ----------------

import sqlite3
import pandas as pd 

class QnAStatus():
    def __init__(self,status):
        self.status = status
        
    def setStatus(self,status):
        self.status = status
    
    def getStatus(self):
        return self.status

qNa = QnAStatus("text")

def readExcel():
    df = pd.read_excel("FaQSheet.xlsx")
    
    chatID = df["chatID"].values
    fieldID = df["Field"].values
    ques = df["Question"].values
    ans = df["Answers"].values
    
    return (chatID,fieldID,ques,ans)
    
def create_field():
    #print(" INto create_field function ")
    value_field = ["Login","Viewing Compliance Tasks","User Roles","Submission of Compliances","Reports","Admin Tasks","Dashboard","Emails","Support"]

    connectn = sqlite3.connect("FaQ.sqlite")
    cursr = connectn.cursor()


    cursr.execute("CREATE TABLE IF NOT EXISTS FaQ(chatID INTEGER , field TEXT )")
    connectn.commit()

    stmt = ("INSERT INTO FaQ (field) VALUES(?)")

    for each in value_field:
        cursr.execute(stmt,(each,))
        connectn.commit()    

def create_FnQ():
    #print("Into create_FnQ function ")
    
    connectn = sqlite3.connect("QnA.sqlite")
    cursr = connectn.cursor()
    
    cursr.execute("CREATE TABLE IF NOT EXISTS QnA(chatID INTEGER , field TEXT , question TEXT , answer TEXT )")
    connectn.commit()
    
    (chatID,fieldID,ques,ans) = readExcel()
    for each in range(1,44):
        stmt = ("INSERT INTO QnA (chatID,field,question,answer) VALUES(?,?,?,?)")
        args = (chatID[each],fieldID[each],ques[each],ans[each])
        
        cursr.execute(stmt,args)
        connectn.commit()

def get_Field_Keyboard():
    connectn = sqlite3.connect("FaQ.sqlite")

    
    stmt = "SELECT field FROM FaQ "
    return [x[0] for x in connectn.execute(stmt)]

def get_QnA_Keyboard(field):
    #connectn = sqlite3.connect("QnA.sqlite")
    #crsr = connectn.cursor()
    
    #stmt = "SELECT question FROM QnA WHERE field = ?"
    #args = (field,)
    
    #crsr.execute(stmt,args)
    #print(crsr.fetchall())
    #return [x[0] for x in connectn.execute(stmt,args)]
	
    returnList = []
    global status
    (chatID,fieldID,ques,ans) = readExcel()
    for each in range(1,44):
        if qNa.getStatus() == "question":
            if fieldID[each] == field:
                returnList.append(ques[each])
        elif qNa.getStatus() == "answer":
            if ques[each] == field:
                returnList.append(ans[each])      
    return returnList
	
##----------------------    Remove and put this code into module ----------------

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def handle_updates(updates):
    listA = ["Login ","Viewing Compliance Tasks","User Roles","Submission of Compliances","Reports","Admin Tasks","Dashboard","Emails","Support", "All FaQ"]
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            if text == "/continue":
                keyboardA = build_keyboard(listA)
                send_message("Please choose a field", chat, keyboardA)
                qNa.setStatus("question")
            elif ( text == "/start" or "hi" == text.lower()):
                send_message(" Welcome to Frequently Asked Questions about compliance manager ", chat)
                #db.add_owner(chat)
                keyboard = build_keyboard(listA)
                #print(" Sab chalta hai ")
                send_message("Please choose a field", chat, keyboard)
                qNa.setStatus("question")
            elif text.startswith("/"):
                continue
            elif  qNa.getStatus() == "question":
                question = get_QnA_Keyboard(text)
                keyboardQ = build_keyboard(question)
                send_message("Pick your question ",chat, keyboardQ)
                qNa.setStatus("answer")
            elif qNa.getStatus() == "answer" :
                answer = get_QnA_Keyboard(text)
                print(answer)
                send_message(answer,chat)
                qNa.setStatus("text")
                time.sleep(3.0)
                send_message("select /continue to check more FaQ ", chat)
        except KeyError:
            pass

def send_message(text, chat_id, reply_markup=None):
    #text = quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)
    
def main():
    last_update_id = None
    qNa.setStatus("text")
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)
    

if __name__ == '__main__':
    main()
    