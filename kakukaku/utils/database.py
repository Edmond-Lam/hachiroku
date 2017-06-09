import hashlib
import sqlite3
import os

DIR = os.path.dirname(__file__)
DIR = DIR[:DIR.index("utils")] + "/"

# check_login takes a parameter for username and a hashed password
# returns a boolean indicating whether the username-password pair is valid
def check_login(username, hashed_pw):
    path = DIR + "data/data.db"
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
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    insert = "INSERT INTO users VALUES (?,?,?,?)"
    curse.execute(insert,(hash(username), username, hashed_pass, 0))
    database.commit()
    database.close()
    return True

def get_user_id(username):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # get user id
    user_query = "SELECT user_id FROM users WHERE username = ?"
    user_result = curse.execute(user_query,(username,))
    user_result = user_result.fetchone()
    print "USER RESULT:", user_result
    if user_result == None:
        return -1
    user_id = int(user_result[0])
    return user_id

def get_username(userid):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # get user id
    if userid == None:
        return None
    user_query = "SELECT username FROM users WHERE user_id = ?"
    user_result = curse.execute(user_query,(userid,))
    user_result = user_result.fetchone()[0]
    print "USER RESULT:", user_result
    if user_result == None:
        return -1
    return user_result

# matches_available takes no parameters
# returns a boolean indicating whether matches exist
def matches_available(uname):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    db_result = {}
    query =  'SELECT match_id FROM matches WHERE user_1 != ? and (pic_2 is NULL OR pic_1 is NULL) and user_2 IS NULL'
    #query = 'SELECT match_id FROM matches WHERE pic_2 is NULL OR pic_1 is NULL and user_1 IS NOT ?'
    #query =  "SELECT * FROM matches WHERE user_2 is NULL and user_1 IS NOT ?
    db_result = curse.execute(query, (get_user_id(uname),))
    #db_result = curse.execute(query, (get_user_id(uname),get_user_id(uname)))
    db_result = db_result.fetchall()
    print "AVAILABLE MATCH", str(db_result)
    return db_result != None and len(db_result) > 0
    '''if not db_result:
        return False
    return True'''


# get_existing_match takes no parameters
# it returns a list of dicts with keys 'word' and 'match_id'
def get_existing_match(uname):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    query =  'SELECT match_id FROM matches WHERE user_1 != ? and (pic_2 is NULL OR pic_1 is NULL)'
    #query =  'SELECT match_id FROM matches WHERE user_1 != ? and user_2 != ? and (pic_2 is NULL OR pic_1 is NULL)'
    db_result = curse.execute(query, (get_user_id(uname),))
    #db_result = curse.execute(query, (get_user_id(uname),get_user_id(uname)))
    ###THIS LINE SOMETIMES GET NONETYPE ERROR BECAUSE YOU CAN'T
    ### DO [0] IF DB_RESULT.FETCHONE() IS NONE
    db_result = db_result.fetchone()[0]
    print "MATCH_RESULT: ", db_result
    return get_match(db_result)


# test
# print get_existing_match()

# make_new_match takes a word and the username of the player who started it
# it returns the match_id of the new match being inserted into the database
def make_new_match(word, username):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # this seems like a good way to get unique match ids
    # the hash might be unnecessary but it makes cooler ids
    # get user_id
    user_id = get_user_id(username)
    '''if user_id == -1:
        return -1'''
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
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    print match_id
    query = "SELECT match_id FROM matches WHERE match_id = ?" 
    result = curse.execute( query, (match_id,) )
    result = result.fetchone()
    if len(result) > 0:
        return True
    return False

# update_match takes a match id, username, and picture url
# doesn't really need to return anything but return a boolean just in case
def update_user_1(match_id, username):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # get user id
    user_id = get_user_id(username)
    if user_id == -1:
        return -1
    query = "UPDATE matches SET user_1 = ? where match_id = ?" 
    curse.execute(query,(user_id, match_id))
    database.commit()
    database.close()
    return True

def update_user_2(match_id, username):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # get user id
    user_id = get_user_id(username)
    if user_id == -1:
        return -1
    query = "UPDATE matches SET user_2 = ? where match_id = ?" 
    curse.execute(query,(user_id, match_id))
    database.commit()
    database.close()
    return True

def update_pic_1(match_id, pic_url_1):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    query = "UPDATE matches SET pic_1 = ? where match_id = ?"
    curse.execute(query,(pic_url_1, match_id))
    database.commit()
    database.close()
    return True

def update_pic_2(match_id, pic_url_2):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    query = "UPDATE matches SET pic_2 = ? where match_id = ?"
    curse.execute(query,(pic_url_2, match_id))
    database.commit()
    database.close()
    return True


def update_judge(match_id, username):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    # get user id
    #user_id = get_user_id(username)
    if user_id == -1:
        return -1

    query = "UPDATE matches SET judge = ? where match_id = ?" 
    curse.execute(query,(user_id, match_id))
    database.commit()
    database.close()
    return True

#updates matches' winner attribute and users' win count
#usernum is a 1 or 2
def update_winner(match_id, usernum):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    #update winner in matches
    if usernum == 1:
        query = "UPDATE matches SET winner = 1 where match_id = ?"
        curse.execute(query, (match_id,))
        database.commit()
        query_2 = "SELECT user_1 FROM matches where match_id = ?" 
        db_result = curse.execute(query_2, (match_id,))
        winner_id = db_result.fetchone()[0]
        print winner_id
        query_3 = "UPDATE users SET wins = wins + 1 where user_id = ?"
        curse.execute(query_3, (winner_id,))
        database.commit()
        database.close()
    else:
        query = "UPDATE matches SET winner = 2 where match_id = ?"
        curse.execute(query, (match_id,))
        database.commit()
        query_2 = "SELECT user_2 FROM matches where match_id = ?"
        db_result = curse.execute(query_2, (match_id,))
        winner_id = db_result.fetchone()[0]
        print winner_id
        query_3 = "UPDATE users SET wins = wins + 1 where user_id = ?"
        curse.execute(query_3, (winner_id,))
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
def get_judgable_match(uname):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    db_result = {}
    query =  "SELECT match_id FROM matches WHERE (user_1 != ? and user_2 != ?) and (judge IS NULL and winner IS NULL and pic_1 IS NOT NULL and pic_2 IS NOT NULL)"
    db_result = curse.execute(query, (get_user_id(uname), get_user_id(uname)))
    db_result = db_result.fetchone()
    if db_result == None:
        return {}
    print "Judging match ID: ", db_result[0]
    match = get_match(db_result[0])
    return match

    
# get_finished_match takes no parameters
# it returns a dict with the same keys as get_judgable_match but with a winner
def get_finished_match():
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    db_result = {}
    query =  "SELECT word, match_id, user_1, user_2, pic_1, pic_2, winner, judge FROM matches WHERE judge NOT NULL and winner NOT NULL"
    db_result = curse.execute(query)
    db_result = db_result.fetchone()
    return get_match(db_result[0])

# get_match returns a dict like get_finished_match but for a specific match_id
def get_match(match_id):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    db_result = {}
    print match_id
    query =  "SELECT * FROM matches WHERE match_id = " + str(match_id)
    db_result = curse.execute(query)
    db_result = db_result.fetchone()
    #print "MATCH FOUND: ", db_result
    result = {
        'word': db_result[1],
        'match_id': db_result[0],
        'user_1': get_username(db_result[2]),
        'user_2': get_username(db_result[4]),
        'img_1': db_result[3],
        'img_2': db_result[5],
        'winner': db_result[7],
        'judge': db_result[6]
    }
    return result

# get_matches_for_user takes a username
# it returns a list of get_finished_match dicts
def get_matches_for_user(username):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    db_result = {}
    user_id = get_user_id(username)
    query =  "SELECT match_id FROM matches WHERE (user_1 = ? OR user_2 = ?) and pic_1 IS NOT NULL and pic_2 IS NOT NULL" 
    db_result = curse.execute(query,(user_id,user_id))
    match_ids = db_result.fetchall()
    results = []
    for match in match_ids:
        print "FINDING: ", match[0]
        results.append(get_match(match[0]))
    #print results
    return results  


# get_rank takes a username
# it returns the number of wins / whatever other rank we want
def get_rank(username):
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    user_id = get_user_id(username)
    #print user_id
    user_query = "SELECT wins FROM users WHERE user_id = ?"
    user_result = curse.execute(user_query,(user_id,))
    user_result = user_result.fetchone()[0]
    #print "USER RESULT:", user_result
    if user_result == None:
        return -1
    return user_result

# returns 
def get_top_ten_players():
    path = DIR + "data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()
    query = "SELECT username, wins FROM users ORDER BY wins DESC LIMIT 10"
    result = curse.execute(query)
    result = result.fetchall()
    final = []
    for thing in result:
        dic = {}
        dic['username'] = thing[0]
        dic['wins'] = thing[1]
        final.append(dic)
    print final
    return final
