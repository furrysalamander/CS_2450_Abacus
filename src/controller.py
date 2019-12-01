# ===============================================================
# Model-View-Controller Architecture for CS_2450_Abacus
# 
# The Controller handles the logic of the program and ties the
#   Model and the View together
#
# ===============================================================
PYTHONDONTWRITEBYTECODE = 0

from model import *
from view import *
from users import *
from abacus import *

from enum import Enum

class State(Enum):
    NONE = 0
    PRACTICE = 1


class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.window = False
        self.current_user = None
        self.current_state = 0

    def create_program_window():
        self.view.create_window('CS_2450_Abacus - Team 5')
        self.window = True

    def ensure_window(func):
        def inner_func(*args, **kwargs):
            if not self.window:
                self.create_program_window()
            return func(*args, **kwargs)
        return inner_func
    
    # ===============================================================
    # State Execution
    def _start_practice():
        View.draw_topbar('Andrew', 'Abacus Practice')
        View.draw_abacus(Point(View.width/2, 400), 500, 7, True)

    def _run_practice():
        while(not View.mouse_clicked()):
            pass
    def _exit_practice():
        pass
    def run(state):
        pass
    
    # ===============================================================
    # Data control
    def is_user_saved(self, user):
        return self.model.get_user(user.idnum) is not None

    def save_user(self, user):
        if(self.is_user_saved(user)):
            self.model.update_user(user.idnum, user.name, user.password)
            print('Updated user {}'.format(user.name))
        else:
            self.model.create_user(user.idnum, user.name, user.password)
            print('Created new user {}'.format(user.name))

    def load_user(self, userID):
        return self.model.get_user(userID)

    def load_user_all(self):
        return self.model.get_user_all()


if(__name__ == '__main__'):
    c = Controller(Model(), View())

    userA = Student()
    userA.idnum = '1234'
    userA.name = 'Cloud'
    userA.password = 'midgar4life'

    userB = Teacher()
    userB.idnum = '0256'
    userB.name = 'Aerith'
    userB.password = 'flowergirl'

    userC = Admin()
    userC.idnum = '4554'
    userC.name = 'Tifa'
    userC.password = '1-2-punch'

    c.save_user(userA)
    c.save_user(userB)
    c.save_user(userC)
    print(c.load_user('332'))
    print(c.load_user_all())

    