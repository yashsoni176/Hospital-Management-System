import flask
from flask import Flask, render_template, redirect, request
import sqlite3

conn = sqlite3.connect("hospital.db", check_same_thread=False)
cursor = conn.cursor()

listOfTables= conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='HOSPITAL' ").fetchall()

if listOfTables!=[]:
    print("Table Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE HOSPITAL(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT, mobile INTEGER, age INTEGER, address TEXT,   
                            DOB INTEGER, place TEXT, pincode INTEGER); ''')
print("Table has created")

app = Flask(__name__)

@app.route("/", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        getname = request.form["name"]
        getpass = request.form["pass"]
    try:
        if getname == 'admin' and getpass == "12345":
            return redirect("/dashboard")
        else:
            print("Invalid username and password")
    except Exception as e:
        print(e)
        
    return render_template("/login.html")

@app.route("/dashboard", methods = ['GET','POST'])
def dashboard():
    if request.method == 'POST':
        getname = request.form['name']
        getmobile = request.form['mobile']
        getage = request.form['age']
        getaddress = request.form['address']
        getDOB = request.form['DOB']
        getplace = request.form['place']
        getpincode = request.form['pincode']

        print(getname)
        print(getmobile)
        print(getage)
        print(getaddress)
        print(getDOB)
        print(getplace)
        print(getpincode)

    try:
        query = cursor.execute("INSERT INTO HOSPITAL(name,mobile,age,address,DOB,place,pincode)VALUES('"+getname+"','"+getmobile+"','"+getage+"','"+getaddress+"','"+getDOB+"','"+getplace+"','"+getpincode+"')")
        print(query)
        conn.commit()
        return redirect("/viewall")
    except Exception as e:
        print(e)

    return render_template("/dashboard.html")

@app.route("/viewall")
def viewall():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM HOSPITAL")
    result = cursor.fetchall()
    return render_template("viewall.html", student=result)

@app.route("/search", methods =['GET','POST'])
def search():
    if request.method == "POST":
        getmobile = request.form["mobile"]
        print(getmobile)
        try:
            query = "SELECT * FROM HOSPITAL WHERE mobile="+getmobile
            cursor.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Mobile number")
            else:
                return render_template("search.html", stud=result, status = True)

        except Exception as e:
            print(e)

    return render_template("search.html", stud=[], status = False)


@app.route("/delete", methods =['GET','POST'])
def delete():
    if request.method == "POST":
        getmobile = request.form['mobile']
        print(getmobile)
        try:
            conn.execute("DELETE FROM HOSPITAL WHERE mobile="+getmobile)
            print("SUCCESSFULLY DELETED!")
            conn.commit()
            return redirect("/viewall")
        except Exception as e:
            print(e)
    return flask.render_template("delete.html")

@app.route("/update", methods =['GET','POST'])
def update():
    if request.method == "POST":
        getmobile = request.form["mobile"]
        print(getmobile)
        try:
            query = "SELECT * FROM HOSPITAL WHERE mobile="+getmobile
            cursor.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Mobile number")
            else:
                return redirect("/viewupdate")

        except Exception as e:
            print(e)

    return render_template("update.html")

@app.route("/viewupdate", methods =['GET','POST'])
def vieupdate():
    if request.method == 'POST':
        getname = request.form['name']
        getmobile = request.form['mobile']
        getage = request.form['age']
        getaddress = request.form['address']
        getDOB = request.form['DOB']
        getplace = request.form['place']
        getpincode = request.form['pincode']

    try:
        cursor.execute("UPDATE HOSPITAL SET name='"+getname+"',mobile='"+getmobile+"',age='"+getage+"',address='"+getaddress+"',DOB='"+getDOB+"',place='"+getplace+"',pincode='"+getpincode+"'WHERE mobile="+getmobile)
        conn.commit()
        return redirect("/viewall")
    except Exception as e:
        print(e)

    return render_template("/viewupdate.html")

if(__name__) == "__main__":
    app.run(debug=True)
