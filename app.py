from cmath import exp
from flask import Flask, render_template,request,url_for,redirect,session
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import pande_db
import random
import uuid
from flask import jsonify
from auth.RtcTokenBuilderSample import getTokenForUser
app = Flask(__name__,template_folder='templates',static_folder="static")
app.secret_key = "dupadupadupa"
pande_db.setup_db(app)
mysql = MySQL(app)

awaiting_users = set([])
logged_users = dict([])
def getSessionAsStr():
    out = ""
    for v,k in session.items():
        out += v + ";" + k + "\n";
    return out

@app.route("/register_form")
def register_form():
    return render_template("register.html");
@app.route("/login_form")
def login_form():
    return render_template("login.html");
@app.route("/login",methods=['POST'])
def login():

    username = request.form['username']
    password = request.form['password']
    userInfo = pande_db.getUserInfo(mysql,username)
    print(userInfo)
    if(len(userInfo) == 1):
        if(sha256_crypt.verify(password,userInfo[0]["password"])):
            session["username"] = username;
            logged_users[username] = {}
            print(logged_users)
            return "login succesfull "+getSessionAsStr() +"\n"; 
        else:
            return "bad password"
    else:
        return "no user with that login"
@app.route("/logout",methods=['GET'])
def logout():
    del logged_users[session['username']]
    session.clear()
    return "logged off"
@app.route("/register",methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    print(username,password)
    if(len(password)<8):
        return "password should be at least 8 letters or longer"
    userInfo = pande_db.getUserInfo(mysql,username)
    print(userInfo)
    if len(userInfo) == 0:
        print(userInfo)
        pande_db.addUser(mysql,username, sha256_crypt.hash(password))
    else:
        return "user already registered";
    return "register succesfull"

@app.route("/join")
def join():
    username = session['username']
    awaiting_users.add(username)
    return "joined"
@app.route("/talk")
def talk():
    print(session['username'])
    return render_template("call.html",userId = session['username'])
@app.route("/checkmatch")
def checkMatch():
    print(logged_users);
    print(session['username'])
    if 'matched' in logged_users[session['username']]:
        return jsonify({
        "channel":logged_users[session['username']]['channel'],
        "token":getTokenForUser(session['username'],logged_users[session['username']]['channel'])
        })
    possible = set([])
    for person in awaiting_users:
        if person != session['username'] and not 'matched' in logged_users[person]:
            possible.add(person)
    print(len(possible))
    if len(possible) == 0:
        print("x")
        return "NO_MATCH"
    match = random.choice(list(possible))
    logged_users[session['username']]['matched'] = True
    logged_users[match]['matched'] = True
    logged_users[session['username']]['channel'] = logged_users[match]['channel'] = str(uuid.uuid4())
    awaiting_users.remove(match)
    awaiting_users.remove(session['username'])
    return jsonify({
        "channel":logged_users[session['username']]['channel'],
        "token":getTokenForUser(session['username'],logged_users[session['username']]['channel'])
    })
@app.route("/leavematch")
def leaveMatch():
    pass
def getToken():
    return getTokenForUser(session['username'])
if __name__ == "__main__":
    app.run(debug=True)