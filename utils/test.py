import sqlite3

def get_user_id(username):
    path = "../data/data.db"
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
    path = "../data/data.db"
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


def update_winner(match_id, usernum):
    path = "../data/data.db"
    database = sqlite3.connect(path)
    curse = database.cursor()

    #update winner in matches
    if usernum == 1:
        query = "UPDATE matches SET winner = 1 where match_id = " + str(match_id)
        curse.execute(query)
        database.commit()

        query_2 = "SELECT user_1 FROM matches where match_id = " + str(match_id)
        db_result = curse.execute(query_2)
        winner_id = db_result.fetchone()[0]
        print winner_id

        query_3 = "UPDATE users SET wins = wins + 1 where user_id = " + str(winner_id)
        curse.execute(query_3)
        database.commit()
        database.close()

    else:
        query = "UPDATE matches SET winner = 2 where match_id = " + str(match_id)
        curse.execute(query)
        database.commit()

        query_2 = "SELECT user_2 FROM matches where match_id = " + str(match_id)
        db_result = curse.execute(query_2)
        winner_id = db_result.fetchone()[0]
        print winner_id

        query_3 = "UPDATE users SET wins = wins + 1 where user_id = " + str(winner_id)
        curse.execute(query_3)
        database.commit()
        database.close()

    return True

#update_winner(6, 1)