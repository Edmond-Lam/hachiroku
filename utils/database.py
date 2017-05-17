import hashlib
import sqlite3

# hashes password
def hash(password):
	h = hashlib.sha256()
	h.update(password)
	return h.hexdigest()

# check_login takes a parameter for username and a hashed password
# returns a boolean indicating whether the username-password pair is valid
def check_login(username, unhashed_pass):
    hashed_pw = hash(unhashed_pass)
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
def create_user(username, unhashed_pass):
	path = "data/data.db"
	database = sqlite3.connect(path)
	curse = db.cursor()
	insert = "INSERT INTO users VALUES ('%s', '%s', '%s')" % (username, hash(unhashed_pass), 0)
	curse.execute(insert)
	database.commit()
	database.close()
    return True
