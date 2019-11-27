# ===============================================================
# Model-View-Controller Architecture for CS_2450_Abacus
# 
# The Controller handles the logic of the program and ties the
#   Model and the View together
#
# ===============================================================


class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view