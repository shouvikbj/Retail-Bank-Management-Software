import sqlite3

# Getting connection to the DATABASE
con = sqlite3.connect('bank.db', check_same_thread=False)
# Creating DATABASE Cursor()
db = con.cursor()

# createTable()
# Creating "accounts" Table in the DATABASE "bank.db"
def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            aid INTEGER PRIMARY KEY AUTOINCREMENT,
            cid INTEGER NOT NULL,
            type VARCHAR2(1000) NOT NULL,
            amount INTEGER NOT NULL,
            timestamp VARCHAR2(100)
        )
    """)

def enterData(cid,type,amount,timestamp):
    db.execute("INSERT INTO accounts VALUES(NULL,?,?,?,?)",(cid,type,amount,timestamp))
    con.commit()

def getData(aid):
    db.execute("SELECT * FROM accounts WHERE aid=(?)",(aid,))
    accounts = db.fetchall()
    return accounts

def getDataForStatus():
    db.execute("SELECT cid,aid,type,timestamp FROM accounts")
    details = db.fetchall()
    return details

def deleteData(aid):
    db.execute("DELETE FROM accounts WHERE aid=(?)",(aid,))
    con.commit()

def deleteAccounts(cid):
    db.execute("DELETE FROM accounts WHERE cid=(?)",(cid,))
    con.commit()

def getAmount(aid):
    db.execute("SELECT amount FROM accounts WHERE aid=(?)",(aid,))
    amount = db.fetchall()
    return amount

def updateAmount(aid,amount):
    db.execute("UPDATE accounts SET amount=(?) WHERE aid=(?)",(amount,aid))
    con.commit()








# createTable()