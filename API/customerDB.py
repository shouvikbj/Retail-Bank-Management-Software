import sqlite3

# Getting connection to the DATABASE
con = sqlite3.connect('bank.db', check_same_thread=False)
# Creating DATABASE Cursor()
db = con.cursor()

# createTable()
# Creating "customers" Table in the DATABASE "bank.db"
def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            ssn INTEGER NOT NULL,
            name VARCHAR2(1000) NOT NULL,
            age INTEGER NOT NULL,
            address VARCHAR2(5000) NOT NULL,
            city VARCHAR2(100) NOT NULL,
            state VARCHAR2(100) NOT NULL
        )
    """)

def enterData(ssn,name,age,address,city,state):
    db.execute("INSERT INTO customers VALUES(NULL,?,?,?,?,?,?)",(ssn,name,age,address,city,state))
    db.execute("SELECT cid,name FROM customers WHERE ssn=(?)",(ssn,))
    customer = db.fetchall()
    con.commit()
    return customer

def findCustomer(id):
    db.execute("SELECT * FROM customers WHERE (cid=(?) OR ssn=(?))",(id,id))
    customer = db.fetchall()
    return customer

def updateDetails(cid,name,age,address,city,state):
    db.execute("UPDATE customers SET name=(?),age=(?),address=(?),city=(?),state=(?) WHERE cid=(?)",(name,age,address,city,state,cid))
    con.commit()

def deleteData(cid):
    db.execute("SELECT name FROM customers WHERE cid=(?)",(cid,))
    name = db.fetchall()
    db.execute("DELETE FROM customers WHERE cid=(?)",(cid,))
    con.commit()
    return name

def getCustomerName(cid):
    db.execute("SELECT name FROM customers WHERE cid=(?)",(cid,))
    name = db.fetchall()
    return name





# createTable()