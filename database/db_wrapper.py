# -*- coding: utf-8 -*-
__author__ = 'Rico'
import sqlite3


def sql_get_db_connection():
    connection = sqlite3.connect("database/users.db")
    connection.text_factory = lambda x: str(x, 'utf-8', "ignore")
    return connection


def sql_connect():
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM users")
    temp_list = []

    result = cursor.fetchall()
    for r in result:
        temp_list.append(list(r))

    connection.close()
    return temp_list


def sql_get_user(user_id):
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM users WHERE userID=?;", [str(user_id)])

    result = cursor.fetchall()
    connection.close()
    if len(result) > 0:
        return result[0]
    else:
        return []


def sql_get_all_users():
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM users;")
    all_users = cursor.fetchall()
    connection.close()
    return all_users


def sql_write(user_id, lang_id, first_name, last_name, username):
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (str(user_id), str(lang_id), str(first_name), str(last_name), str(username), "0", "0", "0", "0"))
    connection.commit()
    connection.close()


def sql_insert(string_value, value, user_id):
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET " + str(string_value) + "= ? WHERE userID = ?;", [str(value), str(user_id)])
    connection.commit()
    connection.close()


def check_if_user_saved(user_id):
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT rowid, * FROM users WHERE userID=?;", [str(user_id)])

    result = cursor.fetchall()
    connection.close()
    if len(result) > 0:
        return result[0]
    else:
        return -1


def get_playing_users(last_played):
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE lastPlayed>=?;", [str(last_played)])
    result = cursor.fetchone()
    connection.close()
    return result[0]


def get_last_players_list():
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users ORDER BY lastPlayed DESC LIMIT 10;")
    result = cursor.fetchall()
    return_text = ""

    connection.close()

    for r in result:
        return_text += str(r[0]) + " | " + str(r[2]) + " | " + str(r[3]) + " | @" + str(r[4]) + " | Spiele: " + str(r[5]) + " | Gew: " + str(r[6]) + " (" + str(r[1]) + ")\n"
    return return_text


def user_data_changed(user_id, first_name, last_name, username):
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE userID=?;", [str(user_id)])

    result = cursor.fetchone()

    connection.close()

    if result[2] == first_name and result[3] == last_name and result[4] == username:
        return False

    return True


def set_user_data(user_id, first_name, last_name, username):
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET first_name=?, last_name=?, username=? WHERE userID=?;", (str(first_name), str(last_name), str(username), str(user_id)))
    connection.commit()
    connection.close()


def reset_stats(user_id):
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET gamesPlayed='0', gamesWon='0', gamesTie='0', lastPlayed='0' WHERE userID=?;", [str(user_id)])
    connection.commit()
    connection.close()


def get_admins():
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM admins;")
    admins = cursor.fetchall()
    connection.close()

    keys = ["user_id", "first_name", "username"]
    admin_dict = []

    for user in admins:
        admin_dict.append(dict(zip(keys, user)))

    return admin_dict


def get_admins_id():
    tmp_list = []
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT userID FROM admins;")
    admins = cursor.fetchall()
    connection.close()

    for admin in admins:
        for userID in admin:
            tmp_list.append(userID)

    return tmp_list


def add_admin(user_id, first_name="", username=""):
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO admins VALUES (?, ?, ?);", (user_id, first_name, username))
    connection.commit()
    connection.close()
    return 0


def rm_admin(user_id):
    connection = sql_get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM admins WHERE userID=?", user_id)
    connection.commit()
    connection.close()
    return 0
