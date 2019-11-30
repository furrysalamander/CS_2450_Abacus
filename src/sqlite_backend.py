# ===============================================================
# Backend server framework for CS_2450_Abacus
# 
# Provides local SQL database for testing and prototyping
#
# ===============================================================


import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
import os

# Setup database name and path
DB_name = 'abacusDB'
DB_path = os.path.dirname(os.path.realpath(__file__)) + '..\\data'


def connect_to_db(db=None):
    if(db == None):
        mydb = ':memory:'
        print('Connecting to in-memory SQLite DB...')
    else:
        mydb = '{}\\{}.db'.format(DB_path, db)
        print('Connecting to SQLite DB...')
    return sqlite3.connect(mydb)

def connect(func):
    def inner_func(conn, *args, **kwargs):
        try:
            conn.execute('SELECT name FROM sqlite_temp_master WHERE type="table";')
        except (AttributeError, ProgrammingError):
            conn = connect_to_db(DB_name)
        return func(conn, *args, **kwargs)
    return inner_func

def disconnect_from_db(conn=None):
    if(not conn == None):
        conn.close()

def scrub(input):
    return ''.join(k for k in input if k.isalnum())

@connect
def create_users_table(conn):
    sql = 'CREATE TABLE users (rowid INTEGER PRIMARY KEY AUTOINCREMENT,' \
          'uid TEXT UNIQUE, name TEXT, password TEXT)'
    try:
        conn.execute(sql)
    except OperationalError as e:
        print(e)

@connect
def insert_user(conn, uid, name, password):
    sql = "INSERT INTO users ('uid', 'name', 'password') VALUES (?, ?, ?)"
    try:
        conn.execute(sql, (uid, name, password))
        conn.commit()
    except IntegrityError as e:
        print('User with uID {} already stored in database'.format(uid))

def tuple_to_dict(mytuple):
    mydict = dict()
    mydict['id'] = mytuple[0]
    mydict['uid'] = mytuple[1]
    mydict['name'] = mytuple[2]
    mydict['password'] = mytuple[3]
    return mydict

@connect
def select_user(conn, uid):
    uid = scrub(uid)
    sql = 'SELECT * FROM users WHERE uid="{}"'.format(uid)
    results = conn.execute(sql)
    user = results.fetchone()
    if(not user == None):
        return tuple_to_dict(user)
    else:
        print('User with uID {} not found in table'.format(uid))

@connect
def select_user_all(conn):
    sql = 'SELECT * FROM users'
    results = conn.execute(sql)
    users = results.fetchall()
    return list(map(lambda x: tuple_to_dict(x), users))

@connect
def update_user(conn, uid, name, password):
    sql_check = 'SELECT EXISTS(SELECT 1 FROM users WHERE uid=? LIMIT 1)'
    sql_update = 'UPDATE users SET name=?, password=? WHERE uid=?'
    results = conn.execute(sql_check, (uid,)) # Need this comma
    user = results.fetchone()
    if(user[0]):
        results.execute(sql_update, (name, password, uid))
        conn.commit()
    else:
        print('User with uID {} not found in table'.format(uid))

@connect
def delete_user(conn, uid):
    uid = scrub(uid)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM users WHERE uid=? LIMIT 1)'
    sql_delete = 'DELETE FROM users WHERE uid=?'
    results = conn.execute(sql_check, (uid,)) # Need this comma
    user = results.fetchone()
    if(user[0]):
        results.execute(sql_delete, (uid,)) # Need this comma
        conn.commit()
    else:
        print('User with uID {} not found in table'.format(uid))



if __name__ == '__main__':
    conn = connect_to_db()
    create_users_table(conn)

    # Adding users
    insert_user(conn, '1001', 'Andrew', 'passrog')
    insert_user(conn, '1002', 'Austin', 'passhuy')
    insert_user(conn, '1003', 'Daniel', 'passmot')
    insert_user(conn, '1004', 'Mike', 'passabb')
    insert_user(conn, '1005', 'Shelby', 'passkon')
    insert_user(conn, '1006', 'Skyler', 'passbal')
    insert_user(conn, '1007', 'Talmage', 'passshu')
    # Trying to add duplicate users
    insert_user(conn, '1006', 'Skyler', 'passbal')
    insert_user(conn, '1007', 'Talmage', 'passshu')
    
    # Selecting users
    print('SELECTING uID 1001')
    print(select_user(conn, '1001'))
    print('SELECTING uID 1002')
    print(select_user(conn, '1002'))
    print('SELECTING uID 1003')
    print(select_user(conn, '1003'))
    print('SELECTING uID 1004')
    print(select_user(conn, '1004'))
    print('SELECTING uID 1005')
    print(select_user(conn, '1005'))
    print('SELECTING uID 1006')
    print(select_user(conn, '1006'))
    print('SELECTING uID 1007')
    print(select_user(conn, '1007'))
    print('SELECTING all users')
    print(select_user_all(conn))

    # Updating users
    print('UPDATING uid 1007')
    update_user(conn, '1007', 'Talwizard', 'youshallnotpass')
    print('SELECTING uID 1007')
    print(select_user(conn, '1007'))

    # Deleting users
    print("DELETING uid 1003")
    delete_user(conn, '1003')
    print('SELECTING uid 1003')
    print(select_user(conn, '1003'))
    print('SELECTING all users')
    print(select_user_all(conn))

    conn.commit()
    conn.close()
