import sqlite3
from random import *

night = True

def insert_player(player_id, username):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"INSERT INTO players (player_id, username) VALUES('{player_id}', '{username}')"
    cur.execute(sql)
    con.commit()
    con.close()

#insert_player(112121, 'nick')

def player_amount():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT * FROM players"
    cur.execute(sql)
    res = cur.fetchall()
    con.close()
    return len(res)

def get_mafia_usernames():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT username FROM players WHERE role = 'mafia'"
    cur.execute(sql)
    res = cur.fetchall()
    names = ''
    for row in res:
        name = row[0]
        names += name + '\n'
    con.close()
    return names

def get_players_role():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT player_id, role FROM players"
    cur.execute(sql)
    res = cur.fetchall()
    con.close()
    return res

def get_all_alive():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT username FROM players WHERE dead = 0"
    cur.execute(sql)
    res = cur.fetchall()
    res = [row[0] for row in res]
    con.close()
    return res

def set_role(players):
    game_roles = ['citizen'] * players
    mafias = int(players * 0.3)
    for i in range(mafias):
        game_roles[i] = 'mafia'
    shuffle(game_roles)
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT player_id FROM players"
    cur.execute(sql)
    players_ids = cur.fetchall()
    for role, row in zip(game_roles, players_ids):
        sql = f"UPDATE players SET role = {role} WHERE player id = {row[0]}"
        cur.execute(sql)
    con.commit()
    con.close()

def vote(type, username, player_id):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT username FROM players WHERE player_id = {player_id} AND dead = 0 AND voted = 0"
    cur.execute(sql)
    user = cur.fetchone()
    if user:
        sql = f"UPDATE players SET {type} = {type} + 1 WHERE username = '{username}'"
        cur.execute(sql)
        sql = f"UPDATE players SET voted = 1 WHERE player_id = '{player_id}'"
        cur.execute(sql)
        con.commit()
        con.close()
        return True
    else:
        con.close()
        return False
    
def mafia_kill():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT MAX(mafia_vote) FROM players WHERE dead = 0"
    cur.execute(sql)
    mafia_vote_max = cur.fetchone()[0]
    print(mafia_vote_max)
    sql = f"SELECT COUNT(*) FROM players WHERE dead = 0 AND role = 'mafia'"
    cur.execute(sql)
    mafia_alive = cur.fetchone()[0]
    kill_name = 'Nobody'
    if mafia_alive == mafia_vote_max:
        sql = f"SELECT username FROM players WHERE mafia_vote = {mafia_vote_max}"
        cur.execute(sql)
        kill_name = cur.fetchone()[0]
        sql = f"UPDATE players SET dead = 1 WHERE username = '{kill_name}'"
        cur.execute(sql)
        con.commit()
    con.close()
    return kill_name

def citizen_kill():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT MAX(citizen_vote) FROM players WHERE dead = 0"
    cur.execute(sql)
    citizen_vote_max = cur.fetchone()[0]
    print(citizen_vote_max)
    sql = f"SELECT COUNT(*) FROM players WHERE dead = 0 AND role = 'citizen'"
    cur.execute(sql)
    citizen_alive = cur.fetchone()[0]
    kill_name = 'Nobody'
    if citizen_alive == citizen_vote_max:
        sql = f"SELECT username FROM players WHERE citizen_vote = {citizen_vote_max}"
        cur.execute(sql)
        kill_name = cur.fetchone()[0]
        sql = f"UPDATE players SET dead = 1 WHERE username = '{kill_name}'"
        cur.execute(sql)
        con.commit()
    con.close()
    return kill_name

def mafia_win():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT COUNT(*) FROM players WHERE dead = 0 AND role = 'mafia'"
    cur.execute(sql)
    mafia_alive = cur.fetchone()[0]
    sql = f"SELECT COUNT(*) FROM players WHERE dead = 0 AND role != 'mafia'"
    cur.execute(sql)
    citizen_alive = cur.fetchone()[0]
    if mafia_alive >= citizen_alive:
        return "Мафия победила"
    if mafia = 0:
        return "Мирные дители победили"



