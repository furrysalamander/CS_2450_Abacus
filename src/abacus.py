# TODO: WHEN METHODS ARE FINISHED, SWITCH
# PASS to RETURN


class Abacus:
    def __init__(self, goal: int = 0, numColumns: int = 5):
        self.goal = goal
        columns = list()
        for i in range(numColumns):
            columns.append(AbacusColumn(0, 0, 0))
        self.columns = columns
        return

    def GetValue(self) -> int:
        """ Returns the integer value of the Abacus. 
        """
        outValue = 0
        for i in range(len(self.columns)):
            outValue += self.columns[i].GetValue() * (10 ** i)
        return outValue

    def SetValue(self, inValue: int):
        """ Sets the integer value of the Abacus.
            The positions of the Abacus beads are adjusted to represent inValue
        """
        if (inValue > self.MaxCapacity()):
            raise OverflowError
        # I'm sure there's a more pythonic way to do this, but here we go.
        newColumnVals = [0] * len(self.columns)
        newColumnIndex = 0
        while(inValue != 0):
            newColumnVals[newColumnIndex] = inValue % 10
            inValue /= 10
            newColumnIndex += 1
            if newColumnIndex > len(self.columns):
                raise OverflowError
        for index, oneNewColumnVal in enumerate(newColumnVals):
            self.SetColumnValue(index, oneNewColumnVal)
    def GetColumnValue(self, index: int):
        """ Returns the current integer value of the specified column.
            Columns are numbered from right to left starting from 0
        """
        # I used index as the parameter name but idk if that's the best way.
        # We just somehow need a way to reference the columns, if you think of
        #   a better way than a list and index value than all the better.
        # Right to left is also not necessary, could be left to right
        return self.columns[index].GetValue() * (10 ** index)

    def SetColumnValue(self, index: int, inValue: int):
        """ Sets the specified column to represent the desired inValue
            Columns are numbered from right to left starting from 0
        """
        self.columns[index].SetValue(inValue)

    def SetGoal(self, value: int):
        """ Sets the value that the user of the Abacus is trying to achieve.
        """
        self.goal = value

    def Validate(self):
        """ Returns True if the current value of the Abacus matches the goal value
            False if otherwise
        """
        return self.GetValue() == self.goal

    def MaxCapacity(self):
        """ Returns the largest number the abacus can hold
        """
        return 10 ** len(self.columns)


class AbacusColumn:
    def __init__(self, numUpperBeads: int = 0, numLowerBeads: int = 0, goal=0):
        self.upper = numUpperBeads
        self.lower = numLowerBeads
        self.goal = goal

    def GetValue(self) -> int:
        """ Returns the integer value of the AbacusColumn
        """
        return self.upper * 5 + self.lower

    def SetValue(self, inValue):
        """ Sets the integer value of the AbacusColumn
            The positions of the beads are adjusted to represent inValue
        """
        self.upper = inValue / 5
        self.lower = inValue % 5
        return

    def ToggleUpper(self, index: int):
        """ Toggles the state of the specified bead in the upper deck.  
            If there are other beads in the way they also get toggled.
        """
        # TODO: check the toggle functions because it's hard for me to visualize this without code to test it.
        # May need some slight adjustments, but I'm pretty sure that the general idea is correct.  Might just need
        # to flip < to > or something like that if it doesn't work.
        if index < self.upper:
            self.upper = index
        else:
            self.upper = 2 - index

    def ToggleLower(self, index: int):
        """ Toggles the state of the specified bead in the lower deck.
            If there are other beads in the way they also get toggled.
        """
        if index < self.upper:
            self.upper = index
        else:
            self.upper = 2 - index

    def SetGoal(self, value: int):
        """ Sets the value that the user of the AbacusColumn is trying to achieve
        """
        self.goal = value

    def Validate(self):
        """ Returns True if the current value of the Abacus matches the goal value
            False if otherwise
        """
        return self.GetValue == self.goal
