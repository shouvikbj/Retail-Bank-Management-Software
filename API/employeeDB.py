import sqlite3

# Getting connection to the DATABASE
con = sqlite3.connect('bank.db', check_same_thread=False)
# Creating DATABASE Cursor()
db = con.cursor()

# createTable()
# Creating "userstore" Table in the DATABASE "bank.db"
def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS userstore(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR2(1000) NOT NULL,
            username VARCHAR2(1000) NOT NULL,
            password VARCHAR2(1000) NOT NULL,
            timestamp VARCHAR2(100),
            image VARCHAR2(200) NOT NULL
        )
    """)

# createEmp(name, username, password)
# Method for creating Bank Employees' Details
def createEmp(name, username, password, image):
    db.execute("INSERT INTO userstore VALUES(NULL,?,?,?,NULL,?)",(name, username, password, image))
    con.commit()

# addTimestamp(username,timestamp)
# Method to track a Employee's last Login Time
def addTimestamp(username, timestamp):
    db.execute("UPDATE userstore SET timestamp=(?) WHERE username=(?)",(timestamp, username))
    con.commit()

# getDetailsForLogin(username)
# Method to provide password for given username for "Login" checking
def getDetailsForLogin(username):
    db.execute("SELECT password FROM userstore WHERE username=(?)",(username,))
    password = db.fetchall()
    return password

# getEmp(username)
# Method to get an Employee based on username
def getEmp(username):
    db.execute("SELECT * FROM userstore WHERE username=(?)",(username,))
    emp = db.fetchall()
    return emp










# createEmp("Abhijit", "avisrkr07@gmail.com", "abhijit@123", "abhijit.jpg")
# createEmp("Shreyasi", "shrschakraborty@gmail.com", "shreyasi@123", "shreyasi.jpg")
# createEmp("Pikolina", "gulmohar2007@gmail.com", "pikolina@123", "pikolina.jpg")
# createEmp("Shouvik", "shouvikbajpayee15@gmail.com", "shouvik@123", "shouvik.jpg")
# createTable()