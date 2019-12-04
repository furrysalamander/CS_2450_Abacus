# ===============================================================
# Backend server framework for CS_2450_Abacus
# 
# Provides local SQL database for testing and prototyping
#
# ===============================================================


import sqlite3
from sqlite3 import OperationalError, IntegrityError, ProgrammingError
import os

# Setup database path
DB_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\\data')

USER_NAMES = ['id', 'uid', 'name', 'password', 'usertype']
CLASS_NAMES = ['id', 'cid', 'name', 'uid']


def connect_to_db(db=None):
    if(db == None):
        mydb = ':memory:'
        #print('Connecting to in-memory SQLite DB...')
    else:
        mydb = '{}\\{}.db'.format(DB_path, db)
        #print('Connecting to SQLite DB...')
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

def tuple_to_dict(mytuple, names):
    mydict = dict()
    for i in range(len(mytuple)):
        mydict[names[i]] = mytuple[i]
    return mydict

@connect
def create_users_table(conn):
    sql = 'CREATE TABLE users (rowid INTEGER PRIMARY KEY AUTOINCREMENT,' \
          'uid TEXT UNIQUE, name TEXT, password TEXT, usertype TEXT)'
    try:
        conn.execute(sql)
        #print('Creating new table users')
    except OperationalError as e:
        #print('Using table users')
        pass

@connect
def insert_user(conn, uid, name, password, usertype):
    sql = "INSERT INTO users ('uid', 'name', 'password', 'usertype') VALUES (?, ?, ?, ?)"
    try:
        conn.execute(sql, (uid, name, password, usertype))
        conn.commit()
    except IntegrityError as e:
        #print('User with uID {} already stored in database'.format(uid))
        pass

@connect
def select_user(conn, uid):
    uid = scrub(uid)
    sql = 'SELECT * FROM users WHERE uid="{}"'.format(uid)
    results = conn.execute(sql)
    user = results.fetchone()
    if(not user == None):
        return tuple_to_dict(user, USER_NAMES)
    else:
        #print('User with uID {} not found in table'.format(uid))
        pass

@connect
def select_user_all(conn):
    sql = 'SELECT * FROM users'
    results = conn.execute(sql)
    users = results.fetchall()
    return list(map(lambda x: tuple_to_dict(x, USER_NAMES), users))

@connect
def update_user(conn, uid, name, password, usertype):
    sql_check = 'SELECT EXISTS(SELECT 1 FROM users WHERE uid=? LIMIT 1)'
    sql_update = 'UPDATE users SET name=?, password=?, usertype=? WHERE uid=?'
    results = conn.execute(sql_check, (uid,)) # Need this comma
    user = results.fetchone()
    if(user[0]):
        results.execute(sql_update, (name, password, usertype, uid))
        conn.commit()
    else:
        #print('User with uID {} not found in table'.format(uid))
        pass

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
        #print('User with uID {} not found in table'.format(uid))
        pass

@connect
def create_class_table(conn):
    sql = 'CREATE TABLE class (rowid INTEGER PRIMARY KEY AUTOINCREMENT,' \
          'cid TEXT UNIQUE, name TEXT, uid TEXT)'
    try:
        conn.execute(sql)
        #print('Creating new table class')
    except OperationalError as e:
        #print('Using table class')
        pass

@connect
def insert_class(conn, cid, name, uid):
    sql = "INSERT INTO class ('cid', 'name', 'uid') VALUES (?, ?, ?)"
    try:
        conn.execute(sql, (cid, name, uid))
        conn.commit()
    except IntegrityError as e:
        #print('Class with cID {} already stored in database'.format(cid))
        pass

@connect
def select_class(conn, cid):
    cid = scrub(cid)
    sql = 'SELECT * FROM class WHERE cid="{}"'.format(cid)
    results = conn.execute(sql)
    clas = results.fetchone()
    if(not clas == None):
        return tuple_to_dict(clas, CLASS_NAMES)
    else:
        #print('Class with cID {} not found in table'.format(cid))
        pass

@connect
def select_class_all(conn):
    sql = 'SELECT * FROM class'
    results = conn.execute(sql)
    clas = results.fetchall()
    return list(map(lambda x: tuple_to_dict(x, CLASS_NAMES), clas))

@connect
def update_class(conn, cid, name, uid):
    sql_check = 'SELECT EXISTS(SELECT 1 FROM class WHERE cid=? LIMIT 1)'
    sql_update = 'UPDATE class SET name=?, uid=? WHERE cid=?'
    results = conn.execute(sql_check, (cid,)) # Need this comma
    clas = results.fetchone()
    if(clas[0]):
        results.execute(sql_update, (name, uid, cid))
        conn.commit()
    else:
        #print('Class with cID {} not found in table'.format(cid))
        pass

@connect
def delete_class(conn, cid):
    cid = scrub(cid)
    sql_check = 'SELECT EXISTS(SELECT 1 FROM class WHERE cid=? LIMIT 1)'
    sql_delete = 'DELETE FROM class WHERE cid=?'
    results = conn.execute(sql_check, (cid,)) # Need this comma
    clas = results.fetchone()
    if(clas[0]):
        results.execute(sql_delete, (cid,)) # Need this comma
        conn.commit()
    else:
        #print('Class with cID {} not found in table'.format(cid))
        pass


if __name__ == '__main__':
    conn = connect_to_db()
    create_users_table(conn)
    create_class_table(conn)

    # Adding users
    insert_user(conn, '1001', 'Andrew', 'passrog', 'student')
    insert_user(conn, '1002', 'Austin', 'passhuy', 'student')
    insert_user(conn, '1003', 'Daniel', 'passmot', 'student')
    insert_user(conn, '1004', 'Mike', 'passabb', 'student')
    insert_user(conn, '1005', 'Shelby', 'passkon', 'student')
    insert_user(conn, '1006', 'Skyler', 'passbal', 'student')
    insert_user(conn, '1007', 'Talmage', 'passshu', 'student')
    # Trying to add duplicate users
    insert_user(conn, '1006', 'Skyler', 'passbal', 'student')
    insert_user(conn, '1007', 'Talmage', 'passshu', 'student')
    
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
    update_user(conn, '1007', 'Talwizard', 'youshallnotpass', 'student')
    print('SELECTING uID 1007')
    print(select_user(conn, '1007'))

    # Deleting users
    print("DELETING uid 1003")
    delete_user(conn, '1003')
    print('SELECTING uid 1003')
    print(select_user(conn, '1003'))
    print('SELECTING all users')
    print(select_user_all(conn))

    # Adding classes
    insert_class(conn, 'CS1400', 'Intro to Programming', '100')
    insert_class(conn, 'CS1410', 'Some Other Class', '101')
    insert_class(conn, 'CS2600', 'Computer Networks I', '102')
    insert_class(conn, 'CS2450', 'Software Engineering', '103')
    # Trying to add duplicate classes
    insert_class(conn, 'CS2600', 'Computer Networks I', '102')
    insert_class(conn, 'CS2450', 'Software Engineering', '103')
    
    # Selecting classes
    print('SELECTING cID CS1400')
    print(select_class(conn, 'CS1400'))
    print('SELECTING cID CS1410')
    print(select_class(conn, 'CS1410'))
    print('SELECTING cID CS2600')
    print(select_class(conn, 'CS2600'))
    print('SELECTING cID CS2450')
    print(select_class(conn, 'CS2450'))
    print('SELECTING all classes')
    print(select_class_all(conn))

    # Updating classes
    print('UPDATING cid CS1410')
    update_class(conn, 'CS1410', 'Programming I', '101')
    print('SELECTING cID CS1410')
    print(select_class(conn, 'CS1410'))

    # Deleting class
    print('DELETING cid CS1410')
    delete_class(conn, 'CS1410')
    print('SELECTING cid CS1410')
    print(select_class(conn, 'CS1410'))
    print('SELECTING all classes')
    print(select_class_all(conn))

    conn.commit()
    conn.close()
