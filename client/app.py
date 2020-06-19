from flask import Flask,render_template,session,redirect,url_for,jsonify,request,make_response,flash
import requests, json, os
import pdfkit
import io
import csv


app = Flask(__name__, static_url_path='')
app.secret_key = 'this is a secret key'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Route to Home Page
# Login Required
@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        url = "http://127.0.0.1:3000/api/getUser/{}".format(username)
        try:
            response = requests.get(url)
            user = response.json()
            return render_template("index.html", user=user)
        except:
            return "<h1>Could not connect to Database Server.</h1>"
    else:
        return redirect(url_for('login'))

# Route to Login Page
@app.route("/login")
def login():
    return render_template("login.html")

# Route to Login User
@app.route("/getin", methods=["POST"])
def getin():
    username = request.form.get("username")
    password = request.form.get("password")
    user = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post("http://127.0.0.1:3000/api/login", json=user)
        status = response.json()
        if(status['status'] == "success"):
            session['username'] = username
            flash("Successfully logged in.", "primary")
            return redirect(url_for('index'))
        else:
            flash("Invalid Credentials. Try Again.", "danger")
            return redirect(url_for('login'))
    except:
        return "<h1>Could not connect to Database Server.</h1>"

# Route to Create New Customer Page
@app.route("/addCustomer", methods=["GET"])
def addCustomerPage():
    if 'username' in session:
        return render_template("addCustomer.html")
    else:
        return redirect(url_for('login'))

# Route to Submit New Customer Details
@app.route("/createNewCustomer", methods=["POST"])
def createNewCustomer():
    if 'username' in session:
        ssn = request.form.get("ssn")
        name = request.form.get("name")
        age = request.form.get("age")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        customerDetails = {
            "ssn": ssn,
            "name": name,
            "age": age,
            "address": address,
            "city": city,
            "state": state
        }
        try:
            response = requests.post("http://127.0.0.1:3000/api/createCustomer", json=customerDetails)
            added_customer = response.json()
            flash("Customer \"" + added_customer["name"] + "\" created successfully.", "primary")
            return redirect(url_for("addCustomerPage"))
        except:
            return "<h1>Could not connect to Database Server.</h1>"
    else:
        flash("You need to Login first", "warning")
        return redirect(url_for('login'))

@app.route("/viewCustomer")
def viewCustomer():
    if 'username' in session:
        return render_template("searchCustomer.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/editCustomer")
def editCustomer():
    if 'username' in session:
        return render_template("searchCustomer.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/deleteCustomer")
def deleteCustomer():
    if 'username' in session:
        return render_template("searchCustomer.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/searchCustomer", methods=["POST"])
def searchCustomer():
    if 'username' in session:
        id = request.form.get("ssn")
        redirect_url = '/customer/{}'.format(id)
        return redirect(redirect_url)
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/customer/<id>")
def customer(id):
    if 'username' in session:
        url = "http://127.0.0.1:3000/api/customer/{}".format(id)
        response = requests.get(url)
        try:
            customer = response.json()
            if (len(customer)):
                return render_template("viewCustomer.html", customer=customer)
            else:
                flash("This customer doesn't exist in our DATABASE anymore","danger")
                return redirect(url_for('editCustomer'))
        except:
            flash("This customer doesn't exist in our DATABASE anymore","danger")
            return redirect(url_for('editCustomer'))
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/updateCustomer/<id>", methods=["POST"])
def updateCustomer(id):
    if 'username' in session:
        cid = id
        name = request.form.get("name")
        age = request.form.get("age")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        updatedDetails = {
            "cid": cid,
            "name": name,
            "age": age,
            "address": address,
            "city": city,
            "state": state
        }
        url = "http://127.0.0.1:3000/api/customer/{}/update".format(cid)
        response = requests.post(url, json=updatedDetails)
        redirect_url = "/customer/{}".format(cid)
        # status = response.json()
        # if(status['UPDATE STATUS'] == "success"):
        #     flash("Details updated successfully.", "primary")
        #     return redirect(redirect_url)
        # else:
        #     flash("Could not update Details", "danger")
        #     return redirect(redirect_url)
        flash("Details updated successfully.", "primary")
        return redirect(redirect_url)

    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/deleteCustomer/<id>/delete")
def removeCustomer(id):
    cid = id
    url = "http://127.0.0.1:3000/api/customer/{}/delete".format(cid)
    response = requests.post(url)
    resp = response.json()
    flash("Customer \"" + resp['name'] + "\" successfully deleted", "primary")
    return redirect(url_for('deleteCustomer'))

@app.route("/viewCustomerStatus")
def viewCustomerStatus():
    if 'username' in session:
        response = requests.get("http://127.0.0.1:3000/api/getCustomerStatus")
        status = response.json()
        return render_template("customerStatus.html", statuses=status)
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/createAccount")
def createAccount():
    if 'username' in session:
        return render_template("createAccount.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/createNewAccount", methods=["POST"])
def createNewAccount():
    if 'username' in session:
        cid = request.form.get("cid")
        type = request.form.get("type")
        amount = request.form.get("amount")
        data = {
            "cid": cid,
            "type": type,
            "amount": amount
        }
        response = requests.post("http://127.0.0.1:3000/api/createAccount", json=data)
        resp = response.json()
        if(resp['status'] == "success"):
            flash("Account for \""+ resp['name'] +"\" created successfully", "primary")
            return redirect(url_for('createAccount'))
        else:
            flash(resp['message'], "danger")
            return redirect(url_for('createAccount'))    
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/deleteAccount")
def deleteAccount():
    if 'username' in session:
        return render_template("searchAccount.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/searchAccount")
def searchAccount():
    if 'username' in session:
        return render_template("searchAccount.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/searchForAccount", methods=["POST"])
def searchAnAccount():
    if 'username' in session:
        id = request.form.get("aid")
        redirect_url = '/account/{}'.format(id)
        return redirect(redirect_url)
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/account/<id>")
def account(id):
    if 'username' in session:
        url = "http://127.0.0.1:3000/api/account/{}".format(id)
        response = requests.get(url)
        data = response.json()
        if(data['status'] == "ok"):
            return render_template("account.html", data=data)
        else:
            flash("This account doesn't exists.", "danger")
            return redirect(url_for('searchAccount'))
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/account/<id>/delete")
def deleteAnAccount(id):
    if 'username' in session:
        url = "http://127.0.0.1:3000/api/account/{}/delete".format(id)
        response = requests.post(url)
        data = response.json()
        if(data['status'] == "ok"):
            flash("Account \""+ data['aid'] +"\" deleted successfully", "primary")
            return redirect(url_for('searchAccount'))
        else:
            flash("This account doesn't exists.", "danger")
            return redirect(url_for('searchAccount'))
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/viewAccountStatus")
def viewAccountStatus():
    if 'username' in session:
        response = requests.get("http://127.0.0.1:3000/api/getAccountStatus")
        status = response.json()
        return render_template("accountStatus.html", statuses=status)
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/deposit")
def searchForDeposit():
    if 'username' in session:
        return render_template("searchForDeposit.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/searchDeposit", methods=["POST"])
def depositScreenRedirection():
    if 'username' in session:
        aid = request.form.get("aid")
        redirect_url = "/deposit/account/{}".format(aid)
        return redirect(redirect_url)
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/deposit/account/<aid>")
def depositScreen(aid):
    if 'username' in session:
        url = "http://127.0.0.1:3000/api/searchAccount/{}".format(aid)
        response = requests.get(url)
        data = response.json()
        if(data['status'] == "ok"):
            return render_template("depositScreen.html", data=data)
        else:
            flash("This Account doesn't exist on our DATABASE", "danger")
            return redirect(url_for('searchForDeposit'))
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/deposit/account/<aid>/deposit", methods=["POST"])
def deposit(aid):
    if 'username' in session:
        amount = {
            "amount": request.form.get("amount")
        }
        redirect_url = "/deposit/account/{}".format(aid)
        url = "http://127.0.0.1:3000/api/searchAccount/{}/deposit".format(aid)
        response = requests.post(url, json=amount)
        resp = response.json()
        if(resp['status'] == "ok"):
            flash("Amount successfully credited to account \""+aid+"\"", "primary")
            return redirect(redirect_url)
        else:
            flash("Amount could not be credited","warning")
            return redirect(redirect_url)

    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))






@app.route("/withdraw")
def searchToWithdraw():
    if 'username' in session:
        return render_template("searchToWithdraw.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))


@app.route("/searchWithdraw", methods=["POST"])
def withdrawScreenRedirection():
    if 'username' in session:
        aid = request.form.get("aid")
        redirect_url = "/withdraw/account/{}".format(aid)
        return redirect(redirect_url)
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/withdraw/account/<aid>")
def withdrawScreen(aid):
    if 'username' in session:
        url = "http://127.0.0.1:3000/api/searchAccount/{}".format(aid)
        response = requests.get(url)
        data = response.json()
        if(data['status'] == "ok"):
            return render_template("withdrawScreen.html", data=data)
        else:
            flash("This Account doesn't exist on our DATABASE", "danger")
            return redirect(url_for('searchToWithdraw'))
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/withdraw/account/<aid>/withdraw", methods=["POST"])
def withdraw(aid):
    if 'username' in session:
        amount = {
            "amount": request.form.get("amount")
        }
        redirect_url = "/withdraw/account/{}".format(aid)
        url = "http://127.0.0.1:3000/api/searchAccount/{}/withdraw".format(aid)
        response = requests.post(url, json=amount)
        resp = response.json()
        if(resp['status'] == "ok"):
            flash("Amount successfully debited from account \""+aid+"\"", "primary")
            return redirect(redirect_url)
        else:
            flash("Amount could not be debited","warning")
            return redirect(redirect_url)

    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))






@app.route("/transfer")
def searchForTransfer():
    if 'username' in session:
        return render_template("searchForTransfer.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/searchTransfer", methods=["POST"])
def transferScreenRedirection():
    if 'username' in session:
        aid1 = request.form.get("aid1")
        aid2 = request.form.get("aid2")
        redirect_url = "/transfer/{}/{}".format(aid1,aid2)
        return redirect(redirect_url)
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/transfer/<aid1>/<aid2>")
def transferScreen(aid1,aid2):
    if 'username' in session:
        url1 = "http://127.0.0.1:3000/api/searchAccount/{}".format(aid1)
        response1 = requests.get(url1)
        data1 = response1.json()
        url2 = "http://127.0.0.1:3000/api/searchAccount/{}".format(aid2)
        response2 = requests.get(url2)
        data2 = response2.json()
        if(data1['status'] == "ok" and data2['status'] == "ok"):
            return render_template("transferScreen.html", data1=data1, data2=data2)
        else:
            flash("One or Both the Accounts doesn't exist on our DATABASE", "danger")
            return redirect(url_for('searchForTransfer'))
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/transfer/account/<aid1>/<aid2>/transfer", methods=["POST"])
def transfer(aid1,aid2):
    if 'username' in session:
        amount = {
            "amount": request.form.get("amount")
        }
        redirect_url = "/transfer/{}/{}".format(aid1,aid2)
        url1 = "http://127.0.0.1:3000/api/searchAccount/{}/withdraw".format(aid1)
        response1 = requests.post(url1, json=amount)
        resp1 = response1.json()
        url2 = "http://127.0.0.1:3000/api/searchAccount/{}/deposit".format(aid2)
        response2 = requests.post(url2, json=amount)
        resp2 = response2.json()
        if(resp1['status'] == "ok" and resp2['status'] == "ok"):
            flash("Amount successfully Transfered from account \""+aid1+"\" to \""+aid2+"\"", "primary")
            return redirect(redirect_url)
        else:
            flash("Amount could not be Transfered","warning")
            return redirect(redirect_url)

    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))


@app.route("/transactionHistory")
def searchAccuontForTransactionHistory():
    if 'username' in session:
        return render_template("searchForTransaction.html")
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/searchTransaction", methods=["POST"])
def searchScreenRedirection():
    if 'username' in session:
        aid = request.form.get("aid")
        redirect_url = "/transaction/account/{}".format(aid)
        return redirect(redirect_url)
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/transaction/account/<aid>")
def transactionScreen(aid):
    if 'username' in session:
        url = "http://127.0.0.1:3000/api/account/{}/trasactions".format(aid)
        response = requests.get(url)
        data = response.json()
        if(data[0]['status'] == "ok"):
            return render_template("transaction.html", datas=data)
        else:
            flash("No transactions found for this account", "warning")
            return redirect(url_for('searchAccuontForTransactionHistory'))
        # return render_template("transaction.html", data=data)
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/transaction/account/<aid>/download")
def transactionStatementDownload(aid):
    if 'username' in session:
        url = "http://127.0.0.1:3000/api/account/{}/trasactions".format(aid)
        response = requests.get(url)
        data = response.json()
        rendered = render_template("transactionStatement.html", datas=data)
        pdf = pdfkit.from_string(rendered, False)
        filename = "TransactionStatement_"+aid
        resp = make_response(pdf)
        resp.headers['Content-Type'] = 'application/pdf'
        resp.headers['Content-Disposition'] = 'inline; filename={}.pdf'.format(filename)
        return resp
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))

@app.route("/transaction/account/<aid>/csv/download")
def transactionStatementCsvDownload(aid):
    if 'username' in session:
        url = "http://127.0.0.1:3000/api/account/{}/trasactions".format(aid)
        response = requests.get(url)
        datas = response.json()

        csvList = [["Transaction ID","Application ID","Description","Date","Amount"]]
        for data in datas:
            csvList.append([data['tid'],data['aid'],data['desc'],data['timestamp'],data['amount']])
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerows(csvList)
        filename = "TransactionStatement_"+aid
        resp = make_response(si.getvalue())
        resp.headers['Content-Type'] = 'text/csv'
        resp.headers['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(filename)
        return resp
    else:
        flash("Login first", "warning")
        return redirect(url_for('login'))








# Route to Logout User
@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("Successfully logged out.", "success")
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True, port=4000)