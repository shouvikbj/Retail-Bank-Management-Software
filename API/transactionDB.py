import sqlite3

# Getting connection to the DATABASE
con = sqlite3.connect('bank.db', check_same_thread=False)
# Creating DATABASE Cursor()
db = con.cursor()

# createTable()
# Creating "transactions" Table in the DATABASE "bank.db"
def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            tid INTEGER PRIMARY KEY AUTOINCREMENT,
            aid INTEGER NOT NULL,
            desc VARCHAR2(5000) NOT NULL,
            timestamp VARCHAR2(100),
            amount INTEGER NOT NULL
        )
    """)

def enterData(aid,desc,timestamp,amount):
    db.execute("INSERT INTO transactions VALUES(NULL,?,?,?,?)",(aid,desc,timestamp,amount))
    con.commit()

def getData(aid):
    db.execute("SELECT * FROM transactions WHERE aid=(?)",(aid,))
    transactions = db.fetchall()
    return transactions








# createTable()