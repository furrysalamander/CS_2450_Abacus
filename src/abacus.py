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
        """ Returns the integer value of the Abacus. 
        """
        outValue = 0
        for i in range(len(self.columns)):
            outValue += self.columns[i].GetValue() * (10 ** i)
        return outValue

    def SetValue(self, inValue):
        """ Sets the integer value of the Abacus.
            The positions of the Abacus beads are adjusted to represent inValue
        """
        pass
    def GetColumnValue(self, index):
        """ Returns the current integer value of the specified column.
            Columns are numbered from right to left starting from 0
        """
        # I used index as the parameter name but idk if that's the best way.
        # We just somehow need a way to reference the columns, if you think of 
        #   a better way than a list and index value than all the better.
        # Right to left is also not necessary, could be left to right
        return self.columns[index].GetValue() * (10 ** index)

    def SetColumnValue(self, index, inValue):
        """ Sets the specified column to represent the desired inValue
            Columns are numbered from right to left starting from 0
        """
        pass

    def SetGoal(self, value):
        """ Sets the value that the user of the Abacus is trying to achieve.
        """
        pass
    def Validate(self):
        """ Returns True if the current value of the Abacus matches the goal value
            False if otherwise
        """
        return self.GetValue() == self.goal
    def MaxCapacity(self):
        # I don't remember what this one was for...  Maybe it returns the biggest
        #   possible number the abacus can do?  Probably not necessary.
        pass

class AbacusColumn:
    def __init__(self, numUpperBeads, numLowerBeads, goal):
        self.upper = 0
        self.lower = 0
        self.goal = 0
        pass
    def GetValue(self):
        """ Returns the integer value of the AbacusColumn
        """
        pass
    def SetValue(self, inValue):
        """ Sets the integer value of the AbacusColumn
            The positions of the beads are adjusted to represent inValue
        """
        pass
    def ToggleUpper(self, index):
        """ Toggles the state of the specified bead in the upper deck.  
            If there are other beads in the way they also get toggled.
        """
        # An example of this would be if a bead in the middle of a bunch of other beads
        #   needs to move upwards.  Any beads above it also need to move upwards.
        # Using an index value here because I assumed the beads(booleans) would be stored in a list
        pass
    def ToggleLower(self, index):
        """ Toggles the state of the specified bead in the lower deck.
            If there are other beads in the way they also get toggled.
        """
        # Same as above ^^^
        pass
    def SetGoal(self, value):
        """ Sets the value that the user of the AbacusColumn is trying to achieve
        """
        pass
    def Validate(self):
        """ Returns True if the current value of the Abacus matches the goal value
            False if otherwise
        """
        return self.GetValue == self.goal