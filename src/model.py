# ===============================================================
# Model-View-Controller Architecture for CS_2450_Abacus
# 
# The Model handles the persistence of data
#
# ===============================================================


import sqlite_backend


class Model(object):

    def __init__(self):
        self.connection = sqlite_backend.connect_to_db(sqlite_backend.DB_name)
        sqlite_backend.create_users_table(self.connection)

    # Users
    def create_user(self, user_ID, name, password):
        sqlite_backend.insert_user(self.connection, user_ID, name, password)
    def get_user(self, user_ID):
        return sqlite_backend.select_user(self.connection, user_ID)
    def update_user(self, user_ID, name, password):
        sqlite_backend.update_user(self.connection, user_ID, name, password)
    def delete_user(self, user_ID):
        sqlite_backend.delete_user(self.connection, user_ID)

