from controller import *
from model import *
from view import *

if(__name__ == '__main__'):
    c = Controller(Model(), View())
    c.create_window()

    state = 'cts'
    while(state is not None):
        state = c.run(state)

    c.close_window()