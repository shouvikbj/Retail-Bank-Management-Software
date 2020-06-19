import sqlite3

# Getting connection to the DATABASE
con = sqlite3.connect('bank.db', check_same_thread=False)
# Creating DATABASE Cursor()
db = con.cursor()

# createTable()
# Creating "customerStatus" Table in the DATABASE "bank.db"
def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS customerStatus(
            cid INTEGER NOT NULL,
            ssn INTEGER NOT NULL,
            status VARCHAR2(10) NOT NULL,
            message VARCHAR2(100) NOT NULL,
            timestamp VARCHAR2(50) NOT NULL
        )
    """)

def enterData(cid,ssn,status,message,timestamp):
    db.execute("INSERT INTO customerStatus VALUES(?,?,?,?,?)",(cid,ssn,status,message,timestamp))
    con.commit()

def updateData(cid,status,message,timestamp):
    db.execute("UPDATE customerStatus SET status=(?),message=(?),timestamp=(?) WHERE cid=(?)",(status,message,timestamp,cid))
    con.commit()

def getData():
    db.execute("SELECT * FROM customerStatus")
    statuses = db.fetchall()
    return statuses





# createTable()