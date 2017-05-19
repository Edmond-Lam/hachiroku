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
def make_new_match(word, username):
    return hash(word + username)
