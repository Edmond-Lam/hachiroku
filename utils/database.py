import hashlib
import sqlite3

'''# hashes password
def hash(password):
    h = hashlib.sha256()
    h.update(password)
    return h.hexdigest()'''

# check_login takes a parameter for username and a hashed password
# returns a boolean indicating whether the username-password pair is valid
def check_login(username, hashed_pw):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    command = "SELECT username, passhash FROM users WHERE username =='" + username + "';"
    reference = curse.execute(command)

    # cross references data in users table
    for record in reference:
        if record[1] == hashed_pw:
            print "Yay"
            database.close()
            return True
        else:
            print "Nay"
            database.close()
            return False
    return False

# create_user takes a username and password
# returns whether user creation was successful
# should always be true unless a username exists in db
def create_user(username, hashed_pass):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    insert = "INSERT INTO users VALUES (%d, '%s', '%s', '%s')" % (hash(username), username, hashed_pass, 0)
    curse.execute(insert)
    database.commit()
    database.close()
    return True

# matches_available takes no parameters
# returns a boolean indicating whether matches exist
def matches_available():
    return False

# get_existing_match takes no parameters
# it returns a dict with keys 'word' and 'match_id'
def get_existing_match():
    return {'word':'doggo', 'match_id':1248667}

# make_new_match takes a word and the username of the player who started it
# it returns the match_id of the new match being inserted into the database
## Sorry lorenz, i needed to do part of this to check if the other things worked
## Don't worry i still left you with the actual match creation <3
def make_new_match(word, username):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # this seems like a good way to get unique match ids
    # the hash might be unnecessary but it makes cooler ids
    # who wants their match id to be a smol integer.
    # not me
    curse.execute("SELECT * FROM matches")
    amt_of_entries = len(curse.fetchall())+1
    return hash(str(amt_of_entries))

# game_exists takes a match id
# it returns a boolean indicating whether a game with the given id could be found in the database
def game_exists(match_id):
    return False

# update_match takes a match id, username, and picture url
# doesn't really need to return anything but return a boolean just in case
def update_match(match_id, username, pic_url):
    return True

# get_finished_match takes no parameters
# it returns a dict with the following keys:
#   'word' : the word from the match
#   'match_id' : the match id
#   'user_1' and 'user_2' : the usernames of both users
#   'img_1' and 'img_2' : the cloudinary urls of the images
#   'winner' : either 'user_1' or 'user_2'
#   Note: user_1 should own img_1 and the same for user_2 and img_2
def get_judgable_match():
    return {'word':'aardvark', 'user_1':'skilled_artist 123', 'user_2':'amateur doodler', 'img_1':'http://res.cloudinary.com/dhan3kbrs/image/upload/v1495060217/homk034qwc51fpbg50wx.jpg', 'img_2':'http://res.cloudinary.com/dhan3kbrs/image/upload/v1495059847/i7grncmpamkn9bd5y53x.jpg', 'match_id':143959858767}

# get_finished_match takes no parameters
# it returns a dict with the same keys as get_judgable_match but with a winner
def get_finished_match():
    return get_judgable_match().update({'winner':'user_1'})

# get_match returns a dict like get_finished_match but for a specific match_id
def get_match(match_id):
    return get_finished_match()

# pick_winner takes parameters match_id and winner
# it sets the winner for the match in the database
# it returns a boolean because why not
def pick_winner(match_id, winner):
    return True

# get_matches_for_user takes a username
# it returns a list of get_finished_match dicts
def get_matches_for_user(username):
    return get_finished_match()
