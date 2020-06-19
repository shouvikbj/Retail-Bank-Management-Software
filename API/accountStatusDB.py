import sqlite3

# Getting connection to the DATABASE
con = sqlite3.connect('bank.db', check_same_thread=False)
# Creating DATABASE Cursor()
db = con.cursor()

# createTable()
# Creating "customerStatus" Table in the DATABASE "bank.db"
def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS accountStatus(
            cid INTEGER NOT NULL,
            aid INTEGER NOT NULL,
            type VARCHAR2(20) NOT NULL,
            status VARCHAR2(10) NOT NULL,
            message VARCHAR2(100) NOT NULL,
            timestamp VARCHAR2(50) NOT NULL
        )
    """)

def enterData(cid,aid,type,status,message,timestamp):
    db.execute("INSERT INTO accountStatus VALUES(?,?,?,?,?,?)",(cid,aid,type,status,message,timestamp))
    con.commit()

def updateData(aid,status,message,timestamp):
    db.execute("UPDATE accountStatus SET status=(?),message=(?),timestamp=(?) WHERE cid=(?)",(status,message,timestamp,aid))
    con.commit()

def getData():
    db.execute("SELECT * FROM accountStatus")
    statuses = db.fetchall()
    return statuses





# createTable()