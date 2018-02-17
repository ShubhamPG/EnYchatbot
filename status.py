import sqlite3
import pandas as pd 

class QnAStatus():
    
    def __init__(self,status):
        self.connectn_QnA = sqlite3.connect("QnA.sqlite")
        self.connectn_Status = sqlite3.connect("status.sqlite")
        
    def createTable(self):
        self.connectn_Status.execute("CREATE TABLE IF NOT EXISTS status(chatID INTEGER , status TEXT)")
        self.connectn_Status.commit()
         
    def updateStatustable(self,status,chat):
        stmt = (" INSERT INTO status ( status , chatID) VALUES(?,?)")
        args = (status,chat)
        self.connectn_Status.execute(stmt,args)
        self.connectn_Status.commit()
    
    def setStatus(self,status,chat):
        stmt = ("UPDATE status set status = ? WHERE chatID = ? ")
        args = (status,chat)
        self.connectn_Status.execute(stmt,args)
        self.connectn_Status.commit()
    
    def getStatus(self,chat):
        stmt = "SELECT status FROM status WHERE chatID = ? "
        args = (chat,)
        for x in self.connectn_Status.execute(stmt, args):
            return x[0]
    
    def readExcel():
        df = pd.read_excel("FaQSheet.xlsx")
        
        fieldID = df["Field"].values
        ques = df["Question"].values
        ans = df["Answers"].values
        
        return (fieldID,ques,ans)
    
    def create_QnA(self,chat_id):
        print("Into create_QnA function ")
        
        self.connectn_QnA.execute("CREATE TABLE IF NOT EXISTS QnA(chatID INTEGER , field TEXT , question TEXT , answer TEXT , status TEXT)")
        
        (fieldID,ques,ans) = QnAStatus.readExcel()
        
        for each in range(0,44):
            stmt = ("INSERT INTO QnA (chatID,field,question,answer,status) VALUES(?,?,?,?,?)")
            args = (chat_id,fieldID[each],ques[each],ans[each],"text")
            
            self.connectn_QnA.execute(stmt,args)
            self.connectn_QnA.commit()
    
    def get_Field_Keyboard(self,chat_id):
        
        stmt = "SELECT DISTINCT field FROM QnA WHERE chatID = chat_id "
        return [x[0] for x in self.connectn_field.execute(stmt)]
    
    def get_QnA_Keyboard(self,field,chat_id):
        connectn = sqlite3.connect("QnA.sqlite")
        crsr = connectn.cursor()
        
        stmt = "SELECT question FROM QnA WHERE chatID=chat_id AND field = ?"
        args = (field,)
        
        crsr.execute(stmt,args)
        print(crsr.fetchall())
        return [x[0] for x in connectn.execute(stmt,args)]
        