from flask import Flask, render_template, request, redirect, url_for, session
import hashlib, json
import requests as req
from utils import database as db
import random

# CHILL WITH THE ALL CAPS EDMOND LAM

# Declaring app and secret key for session encryption
app = Flask(__name__)
app.secret_key = 'Maddy says hi'

def get_new_word():
    wordl = open('nounlist.txt', 'r')
    noun = random.choice(wordl.read().split())
    wordl.close()
    return noun

# Homepage
# Either redirects to the login page or shows you index.html
@app.route('/')
def mainpage():
    if 'username' in session:
        return render_template('index.html', user=session['username'], rank=db.get_rank(session['username']))
    else:
        return redirect(url_for('login'))

# Draw page
# The user clicks on the button on the homepage and is sent to this page to submit their drawing
@app.route('/draw')
def draw():
    # If there are matches in the database, select the word and get match info from there
    if db.matches_available(session['username']):
        print "FOUND A MATCH"
        match_info = db.get_existing_match(session['username'])
        print "MATCH INFO: ", match_info
        word = match_info['word']
        match_id = match_info['match_id']
    # Otherwise, pick a random word and make a match with that word with current user as user_1
    else:
        word = get_new_word()
        match_id = db.make_new_match(word, session['username'])
    # Store the match_id and username for upload
    session['match_id'] = match_id
    return render_template('match.html', word=word)

# Judging page
# If you get the page you're given two photos from a match without a winner
# If you post to the route, it adds a winner to the match and returns you to the index page
@app.route('/judge', methods=['GET', 'POST'])
def judge():
    # Gets a judgable match and passes it to judge.html
    if request.method == 'GET':
        matchdata = db.get_judgable_match(session['username'])
        #print matchdata
        session['matchdata'] = matchdata
        if matchdata == None or len(matchdata) == 0:
            return redirect(url_for('mainpage'))
        print "JUDGING: ", str(matchdata)
        return render_template('judge.html', matchdata=matchdata)
    # Removes matchdata from the session so it's not cluttered then sets the winner in the database
    else:
        matchid = session.pop('matchdata')['match_id']
        winuser = str(int(request.form['winner']) + 1)
        print "Winning user: ", winuser
        db.update_winner(matchid, winuser)
        matchdata = db.get_match(matchid)
        return redirect(url_for('mainpage'))#render_template('index.html', user=session['username'],rank=db.get_rank(session['username']))

# Profile page
# Displays all of the matches the user submitted to with the winner highlighted somehow
@app.route('/profile/<username>')
def profile(username):
    matches = db.get_matches_for_user(username)
    # print matches
    # Edmond's parents had a little Lam
    # Who's groups devlog was empty like the Sahara desert
    return render_template('profile.html', matches = matches)

# Upload route
# Uploads the photo to cloudinary and then updates the database with the picurl
@app.route('/uploadPic', methods=['POST'])
def upload():
    things = { 'file' : request.form['pic'], 'upload_preset' : 'bf17cjwp' }
    upload = req.post('https://api.cloudinary.com/v1_1/dhan3kbrs/auto/upload', data=things)
    picurl = upload.json()['secure_url']
    if 'match_id' in session:
        match_id = session.pop('match_id')
    # This would be awkward
    else:
        return str(session.keys())
    # If the game exists, update it with the picurl.
    if type(match_id) is not int:
        match_id = match_id[0]
    if db.game_exists(match_id):
        if db.get_match(match_id)['img_1'] == None:
            if db.get_match(match_id)['user_1']==session['username']:
                db.update_pic_1(match_id, picurl)
            else:
                db.update_user_1(match_id, session['username'])
                db.update_pic_1(match_id, picurl)
        else:
            db.update_user_2(match_id, session['username'])
            db.update_pic_2(match_id, picurl)
        #db.update_match(match_id, session['username'], picurl)
    return redirect(url_for('mainpage'))#picurl + "<br>" + str(match_id)

@app.route('/gallery', methods=['GET','POST'])
def gallery():
    return render_template('gallery.html', user=session['username'])

# Login route
# Either shows the login page or validates things
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the page is begotten, show the page
    if request.method == 'GET':
        return render_template('login.html')
    # Otherwise, *shrug*
    else:
        if 'username' in session:
            return redirect(url_for('mainpage'))
        
        username = request.form['user']
        password = hashlib.sha1()
        password.update(request.form['pass'])
        password = password.hexdigest()

        if 'register' in request.form:
            db.create_user(username,str(password))
            # Does not update the devlog
            return render_template('login.html', msg="Successfully registered!", good=True)
        
        elif db.check_login(username, str(password)):
            session['username'] = username;
            return redirect(url_for('mainpage'))
        else:
            return render_template('login.html', msg="Login invalid.", good=False)

@app.route("/leaderboard")
def leaderboard():
    return render_template('leaderboard.html', leaders=db.get_top_ten_players())

# Xinhui did this. I am not koalafied to comment on this code
@app.route("/logout/")
def logout():
    if 'username' not in session:
        redirect(url_for('login'))
    session.pop('username')
    return redirect(url_for("login", msg = "Logged out.", good=True))

# Who actually knows what this does. Some sort of black magic I think
if __name__ == '__main__':
    app.debug = True
    app.run()
