# TODO: WHEN METHODS ARE FINISHED, SWITCH
# PASS to RETURN

class Abacus:
    def __init__(self, goal = 0, numColumns = 5):
        self.goal = goal
        columns = list()
        for i in range(numColumns):
            columns.append(AbacusColumn(0,0,0))
        self.columns = columns
        return

    def GetValue(self):
        outValue = 0
        for i in range(len(self.columns)):
            outValue += self.columns[i].GetValue() * (10 ** i)
        return outValue

    def SetValue(self, inValue):
        pass
    def GetColumnValue(self, index):
        return self.columns[index].GetValue() * (10 ** index)

    def SetColumnValue(self, index, inValue):
        pass
    def SetGoal(self, value):
        pass
    def Validate(self):
        return self.GetValue() == self.goal
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
        return self.GetValue == self.goal
