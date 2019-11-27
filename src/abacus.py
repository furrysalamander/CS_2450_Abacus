# TODO: WHEN METHODS ARE FINISHED, SWITCH
# PASS TO RETURN

class Abacus:
    def __init__(self, goal):
        self.goal = goal
        pass
    def GetValue(self):
        pass
    def SetValue(self, inValue):
        pass
    def GetColumnValue(self, index):
        pass
    def SetColumnValue(self, index, inValue):
        pass
    def SetGoal(self, value):
        pass
    def Validate(self):
        pass
    def MaxCapacity(self):
        pass

class AbacusColumn:
    def __init__(self, numUpperBeads, numLowerBeads, goal):
        self.upper = 0
        self.lower = 0
        self.goal = 0
        pass
    def GetValue(self):
        pass
    def SetValue(self):
        pass
    def ToggleUpper(self, index):
        pass
    def ToggleLower(self, index):
        pass
    def SetGoal(self, value):
        pass
    def Validate(self):
        pass