from flask import Flask, render_template, request, redirect, url_for, session
import hashlib, json
import requests as req
from utils import database as db

app = Flask(__name__)
app.secret_key = 'Maddy says hi'

@app.route('/')
def mainpage():
    if 'username' in session:
        session.pop('username')
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/draw')
def draw():
    return render_template('match.html')

@app.route('/uploadPic', methods=['POST'])
def upload():
    things = { 'file' : request.form['pic'], 'upload_preset' : 'bf17cjwp' }
    upload = req.post('https://api.cloudinary.com/v1_1/dhan3kbrs/auto/upload', data=things)
    response = upload.json()['secure_url']
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if 'username' in session:
            return redirect(url_for('mainpage'))
        
        username = request.form['user']
        password = hashlib.sha1()
        password.update(request.form['pass'])
        password = password.hexdigest()

        if 'register' in request.form:
            db.create_user(username,str(password))
            return render_template('login.html', msg="Successfully Registered!!")
    
        elif db.check_login(username, str(password)):
            session['username'] = username;
            return redirect(url_for('mainpage'))
        else:
            return render_template('login.html', msg="Login invalid.")

if __name__ == '__main__':
    app.debug = True
    app.run()
