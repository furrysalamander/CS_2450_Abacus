# ===============================================================
# Model-View-Controller Architecture for CS_2450_Abacus
# 
# The Controller handles the logic of the program and ties the
#   Model and the View together
#
# ===============================================================


from model import *
from view import *
from users import *
from abacus import *


class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.window = False
        self.current_user = None
        self.abacus = None
        self.state = None
        self.state_start = dict()
        self.state_run = dict()
        self.state_exit = dict()

        self.state_start['practice'] = self._start_practice
        self.state_run['practice'] = self._run_practice
        self.state_exit['practice'] = self._exit_practice

    def create_window(self):
        self.view.create_window('CS_2450_Abacus - Team 5')
        self.window = True

    def close_window(self):
        if(self.window is True):
            self.window = False
            self.view.close_window()

    # ===============================================================
    # State Execution

    def run(self, state):
        if(self.state is not state):
            print('Current: {}  Next: {}'.format(self.state, state))
        if(state is '_exit_'):
            if(self.state is not None):
                self.state_exit[self.state]()
            return None
        if(self.state is not state):
            if(self.state is not None):
                self.state_exit[self.state]()
            self.state_start[state]()
        self.state = state

        return self.state_run[state]()

    def cleanup(self):
        if(self.state is not None):
            self.state_exit[self.state]()
            self.state = None
    
    # Practice
    def _start_practice(self):
        View.draw_topbar('Andrew', 'Abacus Practice')
        View.draw_abacus(Point(View.width/2, 400), 500, 7, True)
        self.abacus = Abacus(0, 7)

    def _run_practice(self):
        def move_bead(bead_name, old, new):
            if(old is not new):
                dist = self.view.components['abacus'].data['movdist']
                bead = self.view.components['abacus'].buttons[bead_name]
                if(new):
                    dist = -1*dist
                if(bead_name[2] is 'u'):
                    dist = -1*dist
                print('    Bead: {}  Old: {}  New: {}  Dist: {}'.format(bead_name, old, new, dist))
                bead.label.move(0, dist)
                bead.rect.move(0, dist)
                bead.ymin += dist
                bead.ymax += dist
        # Check abacus beads 
        if(View.mouse_clicked()):
            clicked = View.get_component_clicked('abacus')
            if(clicked):
                upper, col, pos = View.bead_to_column_index(clicked)
                column = AbacusColumn(2, 5)
                column.upper = self.abacus.columns[col].upper
                column.lower = self.abacus.columns[col].lower
                print()
                if(upper):
                    print('Upper bead in column {} position {} was clicked'.format(col, pos))
                    self.abacus.columns[col].ToggleUpper(pos)
                else:
                    print('Lower bead in column {} position {} was clicked'.format(col, pos))
                    self.abacus.columns[col].ToggleLower(pos)
                print('  Old Value: {}  Old Upper: {}  Old Lower: {}'\
                        .format(column.GetValue(), column.upper, column.lower))
                print('  New Value: {}  New Upper: {}  New Lower: {}'\
                        .format(self.abacus.columns[col].GetValue(),
                                self.abacus.columns[col].upper,
                                self.abacus.columns[col].lower))
                for i in range(2):
                    old = column.GetUpperBeadState(i)
                    new = self.abacus.columns[col].GetUpperBeadState(i)
                    move_bead('c' + str(col) + 'u' + str(i), old, new)
                for i in range(5):
                    old = column.GetLowerBeadState(i)
                    new = self.abacus.columns[col].GetLowerBeadState(i)
                    move_bead('c' + str(col) + 'l' + str(i), old, new)
                self.view.components['abacus'].objects['c' + str(col) + 'text']\
                        .setText(str(self.abacus.columns[col].GetValue()))
            clicked = View.get_component_clicked('topbar')
            if(clicked):
                return '_exit_'
        return 'practice'

    def _exit_practice(self):
        View.erase('topbar')
        View.erase('abacus')

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

    # ===============================================================
    # Model Tests
#    userA = Student()
#    userA.idnum = '1234'
#    userA.name = 'Cloud'
#    userA.password = 'midgar4life'

#    userB = Teacher()
#    userB.idnum = '0256'
#    userB.name = 'Aerith'
#    userB.password = 'flowergirl'

#    userC = Admin()
#    userC.idnum = '4554'
#    userC.name = 'Tifa'
#    userC.password = '1-2-punch'

#    c.save_user(userA)
#    c.save_user(userB)
#    c.save_user(userC)
#    print(c.load_user('332'))
#    print(c.load_user_all())#

    # ===============================================================
    # Practice Tests
    c.create_window()

    state = 'practice'
    while(state is not None):
        state = c.run(state)
        pass

    c.close_window()
