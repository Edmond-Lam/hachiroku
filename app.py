from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
from utils import database as db

@app.route("/")
def mainpage():
    if 'username' in session:
        return render_template("home.html")
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("loginpage.html")
    else:
        if 'username' in session:
            return redirect(url_for("mainpage"))
        username = request.form['username']
        password = hashlib.sha1()
        password.update(request.form['password'])
        password = password.hexdigest()
        if db.checkLogin(username, password):
            session['username'] = username;
            return redirect(url_for("mainpage"))
        return render_template("loginpage.html")


@app.route("/register", methods=['POST'])
def register():
    if('username' in session):
        return redirect(url_for("mainpage"))
    username = request.form['username']
    password = hashlib.sha1()
    password.update(request.form['password'])
    password = password.hexdigest()
    db.createUser(username,str(password))
    return render_template("loginpage.html")
