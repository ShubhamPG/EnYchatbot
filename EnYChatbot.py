import json 
import requests
import time 
#import urllib
import nltk
from status import QnAStatus

#print("start")
#nltk.download("punkt")
nltk.download("stopwords")
#print("finish")

TOKEN = "544315494:AAGQ7Oj4gKURC54F_6MdFjQoOW-gZgKNMsk"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

qNa = QnAStatus("text")

##-----------------------------------
            #Email module 
##-----------------------------------
def sendMail(chatID):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
     
     
    fromaddr = "faqboteny@gmail.com"
    toaddr = "chirag_gupta93@yahoo.com,kal1234shubham@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Access approval for EnYBot"
    
    requestMsg = " Hi Anup , Chirag , Shubham \n\n  \tBelow are the Excerpts from the user\n\t "
    for each in qNa.getPermissionMsg(chatID):
        requestMsg += str(each)+",\n\t"
    requestMsg += "ChatID = "+str(chatID)
    requestMsg += " \n\n Regards,\n FaqBot"
    
    body = requestMsg #str(qNa.getPermissionMsg(chatID)) #str(chatID)
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "mizu@1234")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


##-----------------------------------
            #create query formation 
##-----------------------------------
useless_words = nltk.corpus.stopwords.words("english")
start_words = ["who", "what", "when", "where", "why", "how", "is", "can", "does", "do" , "i" , "?"]
templateWords = ["Please","refer","Working","template","'"]
def build_bag_of_words_features_filtered(question):
    #question = question.lower()
    token_words = nltk.word_tokenize(question)
    #token_words = [word for word in token_words if not word in useless_words]
    #token_words = [word for word in token_words if not word in start_words]
    token_words = [word for word in token_words if not word in templateWords]
    return token_words

#build_bag_of_words_features_filtered(ques[0]))

##-----------------------------------

##----------------------    Remove and put this code into module ----------------

chatID_list = []

def get_QnA_Keyboard(field,chat):
    #connectn = sqlite3.connect("QnA.sqlite")
    #crsr = connectn.cursor()
    
    #stmt = "SELECT question FROM QnA WHERE field = ?"
    #args = (field,)
    
    #crsr.execute(stmt,args)
    #print(crsr.fetchall())
    #return [x[0] for x in connectn.execute(stmt,args)]
	
    returnList = []
    global status
    (fieldID,ques,ans) = qNa.readExcel()
    if qNa.getStatus(chat) == "question":
        for each in range(0,11):
            if fieldID[each] == field:
                returnList.append(ques[each])
    elif qNa.getStatus(chat) == "answer":
        for each in range(0,11):
            if ques[each] == field:
                return (ans[each]) 
                break
    return returnList
	
##----------------------    Remove and put this code into module ----------------

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8").replace('\0', '')
    return content


def get_json_from_url(url):
    content = get_url(url)
    #print("In function get_json_from_url")
    if content == "None":
        print("content is none")
    else :
        print("content is OKK")
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

def create_query_table(chatID):
    if chatID in chatID_list:
        return
    else :
        chatID_list.append(chatID)
        qNa.updateStatustable("text",chatID)
    
def isPermission(chatID):
    permissionIDs = qNa.getPermissionIds()
    for each in permissionIDs:
        if chatID == each:
            return True
    return False
            
def handle_update(update):
    listA = [
"Client Requisition",
"Preliminary estimates (PE)",
"Administrative approvals and expenditure sanction",
"Detailed estimates",
"Technical sanction"
]
    try:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        create_query_table(chat)
        
        if(isPermission(chat) == False):
            if ( text == "/start" or "hi" == text.lower()):
                qNa.clearPermissionTable(chat)
                send_message(" Welcome to Frequently Asked Questions about compliance manager ", chat)
                send_message(" You Dont seems to have permission to Access this Bot  ", chat)
                send_message(" Please share your contact details and press /done ", chat)
            elif text == "/done":
                sendMail(chat)
            else:
                qNa.permissionMsg(chat,text)
        elif text == "/continue":
            keyboardA = build_keyboard(listA)
            send_message("Please choose a field", chat, keyboardA)
            qNa.setStatus("question",chat)
        elif ( text == "/start" or "hi" == text.lower()):
            send_message(" Welcome to Frequently Asked Questions about compliance manager ", chat)
            keyboard = build_keyboard(listA)
            send_message("Please choose a field", chat, keyboard)
            qNa.setStatus("question",chat)
        elif text.startswith("/"):
            return
        elif qNa.getStatus(chat) == "question":
            question = get_QnA_Keyboard(text,chat)
            keyboardQ = build_keyboard(question)
            send_message("Pick your question ",chat, keyboardQ)
            qNa.setStatus("answer",chat)
        elif qNa.getStatus(chat) == "answer" :
            #build_bag_of_words_features_filtered(text)
            answer = get_QnA_Keyboard(text,chat)
            send_message(answer,chat)
            send_document(answer,chat)
            qNa.setStatus("text",chat)
            #time.sleep(0.5)
            send_message("select /continue to check more FaQ ", chat)
    except KeyError:
        pass

def handle_updates(updates):
    for update in updates["result"]:
        handle_update(update)
  
def send_message(text, chat_id, reply_markup=None):
    #text = urllib.parse.quote(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)
   
def send_document(text, chat_id, reply_markup=None):
    #curl -F chat_id="468247330" -F document=@"C:\Users\shubham\Downloads\sampleDeploy\EnYchatbot\permissionIDs.xlsx" -F caption="Text Message with attachment" https://api.telegram.org/bot544315494:AAGQ7Oj4gKURC54F_6MdFjQoOW-gZgKNMsk/sendDocument
    docName = decodeText2DocName(text)
    if docName != "None":
        url = URL + "sendDocument?document={}&chat_id={}&parse_mode=Markdown".format(docName, chat_id)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        get_url(url)
   
def decodeText2DocName(text):
    print(text)
    docName = "None"
    if text == ['Please refer Working template 1']:
        docName = "BQADBQADMAADhSMhVUYk3Ed8BgYqAg"
    elif text == ['Please refer Working template 2']:
        docName = "BQADBQADNQADhSMhVTELnFMN3BIDAg"
    return docName
    
def main():
    last_update_id = None
    qNa.createTable()
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.1)
    

if __name__ == '__main__':
    main()
    
