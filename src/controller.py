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
        self.abacus_cur = None
        self.abacus_next = None
        self.selection = None
        self.state = None
        self.state_start = dict()
        self.state_run = dict()
        self.state_exit = dict()

        # Insert states
        self.state_start['practice'] = self._start_practice
        self.state_run['practice'] = self._run_practice
        self.state_exit['practice'] = self._exit_practice
        self.state_start['login'] = self._start_login
        self.state_run['login'] = self._run_login
        self.state_exit['login'] = self._exit_login
        self.state_start['create_user'] = self._start_create_user
        self.state_run['create_user'] = self._run_create_user
        self.state_exit['create_user'] = self._exit_create_user
        self.state_start['tutorial'] = self._start_tutorial
        self.state_run['tutorial'] = self._run_tutorial
        self.state_exit['tutorial'] = self._exit_tutorial
        self.state_start['create_class'] = self._start_create_class
        self.state_run['create_class'] = self._run_create_class
        self.state_exit['create_class'] = self._exit_create_class
        self.state_start['cts'] = self._start_cts
        self.state_run['cts'] = self._run_cts
        self.state_exit['cts'] = self._exit_cts

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
        #if(self.state is not state):
        #    print('Current: {}  Next: {}'.format(self.state, state))
        if(state is '_exit_'):
            if(self.state is not None):
                self.state_exit[self.state]()
            return None
        if(self.state is not state):
            if(self.state is not None):
                self.state_exit[self.state]()
            self.state_start[state]()
        self.state = state

        try:
            return self.state_run[state]()
        except GraphicsError:
            return None

    def cleanup(self):
        if(self.state is not None):
            self.state_exit[self.state]()
            self.state = None
    
    # ===============================================================
    # Abacus
    def _update_bead(self, bead_name, old, new):
        if(old is not new):
            dist = self.view.components['abacus'].data['movdist']
            bead = self.view.components['abacus'].buttons[bead_name]
            if(new):
                dist = -1*dist
            if(bead_name[2] is 'u'):
                dist = -1*dist
            #print('    Bead: {}  Old: {}  New: {}  Dist: {}'.format(bead_name, old, new, dist))
            bead.label.move(0, dist)
            bead.rect.move(0, dist)
            bead.ymin += dist
            bead.ymax += dist
    
    def _update_abacus(self):
        for c in range(len(self.abacus_cur.columns)):
            #print('Updating column {}...'.format(c))
            column_cur = self.abacus_cur.columns[c]
            column_next = self.abacus_next.columns[c]
            #print('  Old Value: {}  Old Upper: {}  Old Lower: {}'\
            #        .format(column_cur.GetValue(), column_cur.upper, column_cur.lower))
            #print('  New Value: {}  New Upper: {}  New Lower: {}'\
            #        .format(column_next.GetValue(), column_next.upper, column_next.lower))
            # Move GUI beads
            for i in range(2):
                old = column_cur.GetUpperBeadState(i)
                new = column_next.GetUpperBeadState(i)
                self._update_bead('c' + str(c) + 'u' + str(i), old, new)
            for i in range(5):
                old = column_cur.GetLowerBeadState(i)
                new = column_next.GetLowerBeadState(i)
                self._update_bead('c' + str(c) + 'l' + str(i), old, new)
            # Update columns cur and next
            column_cur.upper = column_next.upper
            column_cur.lower = column_next.lower
            # Update text
            text = self.view.components['abacus'].objects['c' + str(c) + 'text']
            if(text):
                text.setText(str(column_next.GetValue()))

    def _handle_abacus_click(self, clicked):
        upper, col, pos = View.bead_to_column_index(clicked)
        if(upper):
            #print('Upper bead in column {} position {} was clicked'.format(col, pos))
            self.abacus_next.columns[col].ToggleUpper(pos)
        else:
            #print('Lower bead in column {} position {} was clicked'.format(col, pos))
            self.abacus_next.columns[col].ToggleLower(pos)
        #print('  New column value: {}'.format(self.abacus_next.columns[col].GetValue()))


    # ===============================================================
    # Practice
    def _start_practice(self):
        View.draw_topbar('Andrew', 'Abacus Practice')
        View.set_component_active('topbar', False)
        View.draw_abacus(Point(View.width/2, 400), 500, 7, True)
        self.abacus_cur = Abacus(0, 7)
        self.abacus_next = Abacus(0, 7)

    def _run_practice(self):
        # Check abacus beads 
        if(View.mouse_clicked()):
            clicked = View.get_component_clicked('abacus')
            if(clicked):
                self._handle_abacus_click(clicked)
                self._update_abacus()
            clicked = View.get_component_clicked('topbar')
            if(clicked):
                return '_exit_'
        return 'practice'

    def _exit_practice(self):
        View.erase('topbar')
        View.erase('abacus')

    
    # ===============================================================
    # Login
    def _start_login(self):
        View.draw_login()
    
    def _run_login(self):
        if(View.mouse_clicked()):
            clicked = View.get_component_clicked('login')
            if(clicked is 'login'):
                entered_id = View.components['login'].objects['ide'].getText()
                entered_pass = View.components['login'].objects['passe'].getText()
                if(not self.is_user_saved(entered_id)):
                    print('Invalid ID or password.  Please try again.')
                    return 'login'
                userdata = self.load_user(entered_id)
                if(userdata['password'] == entered_pass):
                    print('Login as {} was successful!'.format(userdata['name']))
                else:
                    print('Invalid ID or password.  Please try again.')
            if(clicked is 'quit'):
                return '_exit_'
        return 'login'

    def _exit_login(self):
        View.erase('login')


    # ===============================================================
    # Create User
    def _create_user_update_options(self, selection):
        options = {'student', 'teacher', 'admin'}
        for op in options:
            if(selection is op):
                View.components['create_user'].objects[op + '_ci'].setOutline('black')
                View.components['create_user'].objects[op + '_ci'].setFill('black')
            else:
                View.components['create_user'].objects[op + '_ci'].setOutline('white')
                View.components['create_user'].objects[op + '_ci'].setFill('white')

    def _start_create_user(self):
        View.draw_topbar('Admin', 'Home | Admin Settings')
        View.set_component_active('topbar', False)
        View.draw_create_user()
        self.selection = 'student'

    def _run_create_user(self):
        if(View.mouse_clicked()):
            clicked = View.get_component_clicked('create_user')
            if(clicked is 'student' or clicked is 'teacher' or clicked is 'admin'):
                self._create_user_update_options(clicked)
                self.selection = clicked
            if(clicked is 'create'):
                entered_name = View.components['create_user'].objects['namee'].getText()
                entered_id = View.components['create_user'].objects['ide'].getText()
                entered_pass = View.components['create_user'].objects['passe'].getText()
                if(len(entered_name) is 0 or len(entered_id) is 0 or len(entered_pass) is 0):
                    print('Can\'t create user with missing fields')
                    return 'create_user'
                if(self.is_user_saved(entered_id)):
                    print('User with that userID already exists')
                    return 'create_user'
                self.save_user(entered_id, entered_name, entered_pass, self.selection)
                print('Added new {} named {} to the database'.format(
                        self.selection, entered_name))
        return 'create_user'

    def _exit_create_user(self):
        View.erase('topbar')
        View.erase('create_user')


    # ===============================================================
    # Tutorial
    def _display_tutorial_page(self, page):
        View.erase('tutorial')
        if(page == 1):
            View.draw_tutorial(
                    'Welcome students! Behold--the UVBacus! \n\nThis is an interactive abacus that is a great way to expand your math skills in a fun and exciting way. It is a whole lot of fun being able to use an abacus and this tutorial will teach you how to do addition and subtraction using the exchange method. \n\nThe abacus will surely make math fun and will provide a neat way to learn the math!',
                    '1',
                    False,
                    True, 
                    0,
                    0,
                    1,
                    0.5,
                    0.7,
                    0.3,
                    13)
        elif(page == 2):
            View.draw_tutorial(
                    'Bead Placement:\n\nThe abacus used in the UVBacus is called a 5:2 abacus. That means that there are 5 beads on the bottom and 2 beads on the top. The abacus has a wall separating the 5 beads on the bottom and the 2 beads on the top.',
                    '2',
                    True,
                    True,
                    0,
                    0,
                    0.65,
                    0.8,
                    0.5,
                    0.85,
                    1)
        elif(page == 3):
            View.draw_tutorial(
                    'More tutorial content coming soon!',
                    '3',
                    True,
                    False,
                    0,
                    0.49,
                    1)

    def _start_tutorial(self):
        View.draw_topbar('Student', 'Tutorial')
        View.set_component_active('topbar', False)
        self.selection = 1
        self._display_tutorial_page(self.selection)

    def _run_tutorial(self):
        if(View.mouse_clicked()):
            clicked = View.get_component_clicked('tutorial')
            if(clicked is 'prev' or clicked is 'next'):
                if(clicked is 'prev'):
                    self.selection -= 1
                if(clicked is 'next'):
                    self.selection += 1
                if(self.selection < 1):
                    self.selection = 1
                if(self.selection > 3):
                    self.selection = 3
                self._display_tutorial_page(self.selection)
        return 'tutorial'

    def _exit_tutorial(self):
        erase('topbar')
        erase('tutorial')


    # ===============================================================
    # Create Class
    def _start_create_class(self):
        View.draw_topbar('Admin', 'Home | Admin Settings')
        View.set_component_active('topbar', False)
        View.draw_create_class()

    def _run_create_class(self):
        if(View.mouse_clicked()):
            clicked = View.get_component_clicked('create_class')
            if(clicked is 'create'):
                entered_id = View.components['create_class'].objects['ide'].getText()
                entered_name = View.components['create_class'].objects['namee'].getText()
                entered_teacher = View.components['create_class'].objects['teachere'].getText()
                if(len(entered_name) is 0 or len(entered_id) is 0 or len(entered_teacher) is 0):
                    print('Can\'t create class with missing fields')
                    return 'create_class'
                if(self.is_class_saved(entered_id)):
                    print('Class with that ID already exists')
                    return 'create_class'
                if(not self.is_user_saved(entered_teacher)):
                    print('Teacher with that ID doesn\'t exist')
                    return 'create_class'
                teacher = self.load_user(entered_teacher)
                if(not teacher['usertype'] == 'teacher'):
                    print('Teacher with that ID doesn\'t exist')
                    return 'create_class'
                self.save_class(entered_id, entered_name, entered_teacher)
                print('Added new class {} taught by {} to the database'.format(
                        entered_name, teacher['name']))
        return 'create_class'

    def _exit_create_class(self):
        View.erase('topbar')
        View.erase('create_class')


    # ===============================================================
    # Connect to Server
    def _start_cts(self):
        View.draw_cts()

    def _run_cts(self):
        if(View.mouse_clicked()):
            clicked = View.get_component_clicked('cts')
            if(clicked == 'connect'):
                entered_server = View.components['cts'].objects['entry'].getText()
                if(len(entered_server) is 0):
                    print('Can\'t connect to server with missing fields')
                    return 'cts'
                print('FUTURE FUNCTIONALITY')
                print('  - Connecting to server named "{}"'.format(entered_server))
            if(clicked == 'quit'):
                return '_exit_'
        return 'cts'

    def _exit_cts(self):
        View.erase('cts')


    # ===============================================================
    # Data control
    def is_user_saved(self, userID):
        return self.model.get_user(userID) is not None

    def save_user(self, userID, name, password, usertype):
        if(self.is_user_saved(userID)):
            self.model.update_user(userID, name, password, usertype)
            #print('Updated user {}'.format(name))
        else:
            self.model.create_user(userID, name, password, usertype)
            #print('Created new user {}'.format(name))

    def load_user(self, userID):
        return self.model.get_user(userID)

    def load_user_all(self):
        return self.model.get_user_all()

    def is_class_saved(self, classID):
        return self.model.get_class(classID) is not None

    def save_class(self, classID, name, teacherID):
        if(self.is_class_saved(classID)):
            self.model.update_class(classID, name, teacherID)
            #print('Updated class {}'.format(name))
        else:
            self.model.create_class(classID, name, teacherID)
            #print('Created new class {}'.format(name))

    def load_class(self, classID):
        return self.model.get_class(classID)

    def load_class_all(self):
        return self.model.get_class_all()



if(__name__ == '__main__'):
    c = Controller(Model(), View())

    c.create_window()

    state = 'create_class'
    while(state is not None):
        state = c.run(state)

    c.close_window()
