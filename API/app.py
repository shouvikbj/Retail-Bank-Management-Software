from flask import Flask, request, jsonify
import datetime as dt
import employeeDB,customerDB,customerStatusDB,accountDB,transactionDB


app = Flask(__name__)
app.secret_key = "TCS_Case_Study"


@app.route("/api/login", methods=["POST"])
def empLogin():
    username = request.json['username']
    provided_password = request.json['password']
    actual_password = employeeDB.getDetailsForLogin(username)
    if(len(actual_password)):
        if(actual_password[0][0] == provided_password):
            curDate = dt.datetime.now()
            day = curDate.strftime("%d-%m-%Y")
            time = curDate.strftime("%H:%M")
            timestamp = day + ", at " + time
            employeeDB.addTimestamp(username, timestamp)
            result = {
                "status": "success",
            }
            return jsonify(result)
        else:
            result = {
                "status": "failed"
            }
            return jsonify(result)
    else:
        result = {
            "status": "failed"
        }
        return jsonify(result)

@app.route("/api/getUser/<username>", methods=["GET"])
def getUser(username):
    emp = employeeDB.getEmp(username)
    user = {
        "id": emp[0][0],
        "name": emp[0][1],
        "username": emp[0][2],
        "timestamp": emp[0][4],
        "image": emp[0][5]
    }
    return jsonify(user)

@app.route("/api/createCustomer", methods=["POST"])
def createCustomer():
    ssn = int(request.json['ssn'])
    name  = request.json['name']
    age = int(request.json['age'])
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    customer = customerDB.enterData(ssn,name,age,address,city,state)
    added_customer = {
        "name": customer[0][1]
    }
    customerId = customer[0][0]
    status = "Active"
    message = "Customer Created Successfully"
    curDate = dt.datetime.now()
    day = curDate.strftime("%d-%m-%Y")
    time = curDate.strftime("%H:%M")
    timestamp = day + ", at " + time
    customerStatusDB.enterData(customerId,ssn,status,message,timestamp)
    return jsonify(added_customer)

@app.route("/api/customer/<id>", methods=["GET"])
def findUser(id):
    got_customer = customerDB.findCustomer(id)
    customer = {
        "cid": got_customer[0][0],
        "ssn": got_customer[0][1],
        "name": got_customer[0][2],
        "age": got_customer[0][3],
        "address": got_customer[0][4],
        "city": got_customer[0][5],
        "state": got_customer[0][6]
    }
    return jsonify(customer)

@app.route("/api/customer/<cid>/update", methods=["POST"])
def updateCustomer(cid):
    cid = int(request.json['cid'])
    name  = request.json['name']
    age = int(request.json['age'])
    address = request.json['address']
    city = request.json['city']
    state = request.json['state']
    customerDB.updateDetails(cid,name,age,address,city,state)
    customerId = cid
    status = "Active"
    message = "Customer Details Updated"
    curDate = dt.datetime.now()
    day = curDate.strftime("%d-%m-%Y")
    time = curDate.strftime("%H:%M")
    timestamp = day + ", at " + time
    customerStatusDB.updateData(cid,status,message,timestamp)
    status = {
        "UPDATE STATUS": "success"
    }
    return jsonify(status)

@app.route("/api/customer/<cid>/delete", methods=["POST"])
def deleteCustomer(cid):
    name = customerDB.deleteData(cid)
    # accountDB.deleteAccounts(cid)
    customer_name = {
        "name": name[0][0]
    }
    customerId = cid
    status = "Deactive"
    message = "Customer Deleted"
    curDate = dt.datetime.now()
    day = curDate.strftime("%d-%m-%Y")
    time = curDate.strftime("%H:%M")
    timestamp = day + ", at " + time
    customerStatusDB.updateData(cid,status,message,timestamp)
    return jsonify(customer_name)

@app.route("/api/getCustomerStatus")
def getCustomerStatus():
    statuses = customerStatusDB.getData()
    customerStatus = []
    for status in statuses:
        cStatus = {
            "cid": status[0],
            "ssn": status[1],
            "status": status[2],
            "message": status[3],
            "timestamp": status[4]
        }
        customerStatus.append(cStatus)
    return jsonify(customerStatus)

@app.route("/api/createAccount", methods=["POST"])
def creaetAccount():
    cid = int(request.json['cid'])
    type = request.json['type']
    amount = int(request.json['amount'])
    curDate = dt.datetime.now()
    day = curDate.strftime("%d-%m-%Y")
    time = curDate.strftime("%H:%M")
    timestamp = day + ", at " + time
    customer_name = customerDB.getCustomerName(cid)
    if(len(customer_name)):
        accountDB.enterData(cid,type,amount,timestamp)
        resp = {
            "status": "success",
            "name": customer_name[0][0]
        }
        return jsonify(resp)
    else:
        resp ={
            "status": "failed",
            "message": "Customer doesn't exists on our DATABASE"
        }
        return jsonify(resp)

@app.route("/api/account/<aid>")
def getAccount(aid):
    data = accountDB.getData(aid)
    if(len(data)):
        aid = data[0][0]
        cid = data[0][1]
        name = (customerDB.getCustomerName(cid))[0][0]
        type = data[0][2]
        amount = data[0][3]

        account = {
            "status": "ok",
            "aid": aid,
            "cid": cid,
            "name": name,
            "type": type,
            "amount": amount
        }
    else:
        account = {
            "status": "No Account Found!"
        }
    return jsonify(account)

@app.route("/api/account/<aid>/delete", methods=["POST"])
def deleteAccount(aid):
    try:
        accountDB.deleteData(aid)
        details = {
            "status": "ok",
            "aid": aid
        }
        return jsonify(details)
    except:
        details = {
            "status": "No Account Found!"
        }
        return jsonify(details)
        
@app.route("/api/getAccountStatus")
def getAccountStatus():
    dataFromAccount = accountDB.getDataForStatus()
    accountStatus = []
    for data in dataFromAccount:
        status = {
            "cid": data[0],
            "aid": data[1],
            "type": data[2],
            "timestamp": data[3],
            "status": "Active",
            "message": "Account created with a specific type"
        }
        accountStatus.append(status)
    return jsonify(accountStatus)


@app.route("/api/searchAccount/<aid>")
def searchDetailsForTransaction(aid):
    accountInfo = accountDB.getData(aid)
    if(len(accountInfo)):
        customerName = customerDB.getCustomerName(accountInfo[0][1])
        if(len(customerName)):
            depositAccount = {
                "status": "ok",
                "aid": accountInfo[0][0],
                "cid": accountInfo[0][1],
                "type": accountInfo[0][2],
                "amount": accountInfo[0][3],
                "name": customerName[0][0]
            }
    else:
        depositAccount = {
            "status": "failed",
            "message": "Account Not Found"
        }
    return jsonify(depositAccount)

@app.route("/api/searchAccount/<aid>/deposit", methods=["POST"])
def addAmount(aid):
    depositAmount = int(request.json['amount'])
    currentAmount = int((accountDB.getAmount(aid))[0][0])
    updatedAmount = currentAmount + depositAmount
    accountDB.updateAmount(aid,updatedAmount)
    curDate = dt.datetime.now()
    day = curDate.strftime("%d-%m-%Y")
    time = curDate.strftime("%H:%M")
    timestamp = day + ", at " + time
    transactionDB.enterData(aid,"Deposit",timestamp,depositAmount)
    resp = {
        "status": "ok"
    }
    return jsonify(resp)

@app.route("/api/searchAccount/<aid>/withdraw", methods=["POST"])
def substractAmount(aid):
    withdrawAmount = int(request.json['amount'])
    currentAmount = int((accountDB.getAmount(aid))[0][0])
    updatedAmount = currentAmount - withdrawAmount
    if(updatedAmount < 0):
        updatedAmount = 0
    accountDB.updateAmount(aid,updatedAmount)
    curDate = dt.datetime.now()
    day = curDate.strftime("%d-%m-%Y")
    time = curDate.strftime("%H:%M")
    timestamp = day + ", at " + time
    transactionDB.enterData(aid,"Withdraw",timestamp,withdrawAmount)
    resp = {
        "status": "ok"
    }
    return jsonify(resp)

@app.route("/api/account/<aid>/trasactions")
def transactions(aid):
    transactions = transactionDB.getData(aid)
    data = []
    if(len(transactions)):
        for transaction in transactions:
            transact = {
                "status": "ok",
                "aid": aid,
                "tid": transaction[0],
                "desc": transaction[2],
                "timestamp": transaction[3],
                "amount": transaction[4]
            }
            data.append(transact)
    else:
        transact = {
            "status": "failed"
        }
        data.append(transact)
    return jsonify(data)












if __name__ == "__main__":
    app.run(debug=True, port=3000)