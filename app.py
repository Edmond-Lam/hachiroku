from flask import Flask, render_template, request, redirect, url_for, session
import hashlib, json
import requests as req
from utils import database as db
import random

app = Flask(__name__)
app.secret_key = 'Maddy says hi'

def get_new_word():
    wordl = open('nounlist.txt', 'r')
    noun = random.choice(wordl.read().split())
    wordl.close()
    return noun

@app.route('/')
def mainpage():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/draw')
def draw():
    if db.matches_available():
        match_info = db.get_existing_match()
        word = match_info['word']
        match_id = match_info['match_id']
    else:
        word = get_new_word()
        match_id = db.make_new_match(word, session['username'])
        
    session['match_id'] = match_id
    return render_template('match.html', word=word)

@app.route('/judge', methods=['GET', 'POST'])
def judge():
    if request.method == 'GET':
        matchdata = db.get_finished_match()
        session['matchdata'] = matchdata
        return render_template('judge.html', matchdata=matchdata)
    else:
        matchdata = session.pop('matchdata')
        winuser = str(int(request.form['winner']) + 1)
        db.pick_winner(matchdata['match_id'], winuser)
        return '<h1>User %s won match %s with:</h1> <img src="%s"/>' % (matchdata['user_' + winuser], matchdata['match_id'], matchdata['img_' + winuser])
        
@app.route('/uploadPic', methods=['POST'])
def upload():
    things = { 'file' : request.form['pic'], 'upload_preset' : 'bf17cjwp' }
    upload = req.post('https://api.cloudinary.com/v1_1/dhan3kbrs/auto/upload', data=things)
    picurl = upload.json()['secure_url']
    if 'match_id' in session:
        match_id = session.pop('match_id')
    else:
        return 'yikes'
    if db.game_exists(match_id):
        db.update_match(match_id, session['username'], picurl)
    return picurl + "<br>" + str(match_id)

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
