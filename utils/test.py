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


def get_top_ten_players():
    path = "../data/data.db"
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

get_top_ten_players()