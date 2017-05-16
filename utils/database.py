import hashlib
import sqlite3

#hashes password
def hash(x):
	h = hashlib.sha256()
	h.update(x)
	return h.hexdigest()

# check_login takes a parameter for username and a hashed password
# returns a boolean indicating whether the username-password pair is valid
def check_login(username, hash_pass):
    return True

# create_user takes a username and password
# returns whether user creation was successful
# should always be true unless a username exists in db
def create_user(username, hash_pass):
    return True
