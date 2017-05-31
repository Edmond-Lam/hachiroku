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
    insert = "INSERT INTO users VALUES (?,?,?,?)"
    curse.execute(insert,(hash(username), username, hashed_pass, 0))
    database.commit()
    database.close()
    return True

def get_username(userid):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # get user id
    user_query = "SELECT username FROM users WHERE user_id = ?"
    user_result = curse.execute(user_query,(userid,))
    user_result = user_result.fetchone()
    print "USER RESULT:", user_result
    if user_result == None:
        return -1
    user_id = int(user_result[0])
    return user_id

# matches_available takes no parameters
# returns a boolean indicating whether matches exist
def matches_available():
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    db_result = {}
    query =  "SELECT * FROM matches WHERE user_2 is NULL"
    db_result = curse.execute(query)
    db_result = db_result.fetchall()
    print db_result
    if not db_result:
        return False
    return True

# get_existing_match takes no parameters
# it returns a list of dicts with keys 'word' and 'match_id'
def get_existing_match():
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    results = []
    query =  'SELECT * FROM matches WHERE pic_2 is NULL OR pic_1 is NULl'
    db_result = curse.execute(query)
    db_result = db_result.fetchone()
    if len(db_result) == 0:
        return {}
    result = {
        'word': db_result[1],
        'match_id': db_result[0],
        'user_1': db_result[2],
        'user_2': db_result[4],
        'img_1': db_result[3],
        'img_2': db_result[5],
        'winner': db_result[7],
        'judge': db_result[6]
    }
    return result

# test
# print get_existing_match()

# make_new_match takes a word and the username of the player who started it
# it returns the match_id of the new match being inserted into the database
def make_new_match(word, username):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # this seems like a good way to get unique match ids
    # the hash might be unnecessary but it makes cooler ids
    # get user_id
    user_id = get_username(username)
    if user_id == -1:
        return -1
    match_query = "INSERT INTO matches (user_1, word) VALUES (?, ?)" 
    # amt_of_entries = len(curse.fetchall())+1
    curse.execute(match_query,(user_id, word))
    database.commit()
    # get new match id
    new_match_id = 0
    new_match_query = "SELECT match_id FROM matches WHERE user_1 = ? AND word = ?"
    new_match_result = curse.execute(new_match_query,(user_id, word))
    new_match_result = new_match_result.fetchall()
    print new_match_result
    new_match_id = new_match_result[0]
    database.close()
    return new_match_id

# game_exists takes a match id
# it returns a boolean indicating whether a game with the given id could be found in the database
def game_exists(match_id):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    query = "SELECT match_id FROM matches WHERE match_id = ?" 
    result = curse.execute(query,(match_id,))
    if len(query) > 0:
        return True
    return False

# update_match takes a match id, username, and picture url
# doesn't really need to return anything but return a boolean just in case
def update_user_2(match_id, username):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # get user id
    user_id = get_username(username)
    if user_id == -1:
        return -1
    query = "UPDATE matches SET user_2 = ? where match_id = ?" 
    curse.execute(query,(user_id, match_id))
    database.commit()
    database.close()
    return True

def update_pic_1(match_id, pic_url_1):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    query = "UPDATE matches SET pic_1 = ? where match_id = ?"
    curse.execute(query,(pic_url_1, match_id))
    database.commit()
    database.close()
    return True

def update_pic_2(match_id, pic_url_2):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    query = "UPDATE matches SET pic_2 = ? where match_id = ?"
    curse.execute(query,(pic_url_2, match_id))
    database.commit()
    database.close()
    return True


def update_judge(match_id, username):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # get user id
    user_id = get_username(username)
    if user_id == -1:
        return -1

    query = "UPDATE matches SET judge = ? where match_id = ?" 
    curse.execute(query,(user_id, match_id))
    database.commit()
    database.close()
    return True

def update_winner(match_id, username):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # get user id
    user_id = get_username(username)
    if user_id == -1:
        return -1

    query = "UPDATE matches SET winner = ? where match_id = ?"
    curse.execute(query,(user_id, match_id))
    database.commit()
    database.close()
    return True

# get_finished_match takes no parameters
# it returns a dict with the following keys:
#   'word' : the word from the match
#   'match_id' : the match id
#   'user_1' and 'user_2' : the usernames of both users
#   'img_1' and 'img_2' : the cloudinary urls of the images
#   'winner' and 'judge' must be NULL
#   Note: user_1 should own img_1 and the same for user_2 and img_2
def get_judgable_match():
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    db_result = {}
    query =  "SELECT * FROM matches WHERE judge IS NULL and winner IS NULL and pic_1 IS NOT NULL and pic_2 IS NOT NULL"
    db_result = curse.execute(query)
    db_result = db_result.fetchone()
    result = {
        'word': db_result[1],
        'match_id': db_result[0],
        'user_1': db_result[2],
        'user_2': db_result[4],
        'img_1': db_result[3],
        'img_2': db_result[5],
        'winner': db_result[7],
        'judge': db_result[6]
    }
    return result

    
# get_finished_match takes no parameters
# it returns a dict with the same keys as get_judgable_match but with a winner
def get_finished_match():
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    db_result = {}
    query =  "SELECT word, match_id, user_1, user_2, pic_1, pic_2, winner, judge FROM matches WHERE judge NOT NULL and winner NOT NULL"
    db_result = curse.execute(query)
    db_result = db_result.fetchone()
    return get_match(db_result[0])

# get_match returns a dict like get_finished_match but for a specific match_id
def get_match(match_id):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    db_result = {}
    query =  "SELECT * FROM matches WHERE match_id = ?"
    db_result = curse.execute(query, (match_id,)).fetchone()
    result = {
        'word': db_result[1],
        'match_id': db_result[0],
        'user_1': db_result[2],
        'user_2': db_result[4],
        'img_1': db_result[3],
        'img_2': db_result[5],
        'winner': db_result[7],
        'judge': db_result[6]
    }
    return result

# pick_winner takes parameters match_id and winner
# it sets the winner for the match in the database
# it returns a boolean because why not
def pick_winner(match_id, winner):
    update_winner(match_id, winner)
    return True

# get_matches_for_user takes a username
# it returns a list of get_finished_match dicts
def get_matches_for_user(username):
    path = "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    db_result = {}
    query =  "SELECT word, match_id, user_1, user_2, pic_1, pic_2, winner, judge FROM matches WHERE user_1 = ? " 
    db_result = curse.execute(query,(username,))
    if not db_result:
        return []
    results = []
    for word, match_id, user_1, user_2, pic_1, pic_2, winner, judge in db_result:
        winner_username = get_username(winner)
        judge_username = get_username(judge)
        result = {
            'word': word,
            'match_id': match_id,
            'user_1': user_1,
            'user_2': user_2,
            'img_1': pic_1,
            'img_2': pic_2,
            'winner': winner_username,
            'judge': judge_username
        }
        results.append(result)
    return results  
