# ===============================================================
# Model-View-Controller Architecture for CS_2450_Abacus
# 
# The Model handles the persistence of data
#
# ===============================================================


import sqlite_backend


class Model(object):

    def __init__(self):
        self.connection = sqlite_backend.connect_to_db('CS_2450_Abacus_Team5')
        sqlite_backend.create_users_table(self.connection)
        sqlite_backend.create_class_table(self.connection)

    # Users
    def create_user(self, user_ID, name, password, usertype):
        sqlite_backend.insert_user(self.connection, user_ID, name, password, usertype)
    def get_user(self, user_ID):
        return sqlite_backend.select_user(self.connection, user_ID)
    def get_user_all(self):
        return sqlite_backend.select_user_all(self.connection)
    def update_user(self, user_ID, name, password, usertype):
        sqlite_backend.update_user(self.connection, user_ID, name, password, usertype)
    def delete_user(self, user_ID):
        sqlite_backend.delete_user(self.connection, user_ID)

    # Classes
    def create_class(self, class_ID, name, teacher_ID):
        sqlite_backend.insert_class(self.connection, class_ID, name, teacher_ID)
    def get_class(self, class_ID):
        return sqlite_backend.select_class(self.connection, class_ID)
    def get_class_all(self):
        return sqlite_backend.select_class_all(self.connection)
    def update_class(self, class_ID, name, teacher_ID):
        sqlite_backend.update_class(self.connection, class_ID, name, teacher_ID)
    def delete_class(self, class_ID):
        sqlite_backend.delete_class(self.connection, class_ID)
