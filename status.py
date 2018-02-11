import sqlite3
import pandas as pd 

class QnAStatus():
    def __init__(self,status):
        self.status = status
        
    def setStatus(self,status):
        self.status = status
    
    def getStatus(self):
        return self.status
    
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
        
        for each in range(0,44):
            stmt = ("INSERT INTO QnA (chatID,field,question,answer) VALUES(?,?,?,?)")
            args = (chatID[each],fieldID[each],ques[each],ans[each])
            
            cursr.execute(stmt,args)
            connectn.commit()
    
    def get_Field_Keyboard():
        connectn = sqlite3.connect("FaQ.sqlite")
    
        
        stmt = "SELECT field FROM FaQ "
        return [x[0] for x in connectn.execute(stmt)]