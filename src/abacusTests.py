
from abacus import *


def showAbacus(abacus):
    for c in range(len(abacus.columns)):
        col = abacus.columns[c]
        line = '   | '
        # Upper beads
        for i in range(2 - col.upper):
            line += '0'
        line += '-'
        for i in range(col.upper):
            line += '0'
        line += ' '
        # Lower beads
        for i in range(col.lower):
            line += '0'
        line += '-'
        for i in range(5 - col.lower):
            line += '0'
        line += ' |'
        # Print result
        print(line)

if(__name__ == '__main__'):
    
    # Create and display an abacus
    abacus = Abacus(0, 3)
    showAbacus(abacus)

    # SetValue
    def setValueTest(abacus, value):
        print("Changing value to {}".format(value))
        abacus.SetValue(value)
    
    # GetValue
    def getValueTest(abacus):
        print('Value of abacus is {}'.format(abacus.GetValue()))
        showAbacus(abacus)
    
    setValueTest(abacus, 234)
    getValueTest(abacus)

    setValueTest(abacus, 700)
    getValueTest(abacus)

    setValueTest(abacus, 5)
    getValueTest(abacus)

    setValueTest(abacus, 999)
    getValueTest(abacus)

    setValueTest(abacus, 549)
    getValueTest(abacus)

    setValueTest(abacus, 0)
    getValueTest(abacus)

    # ToggleUpper
    def toggleUpperTest(abacus, column, index):
        print('Toggling upper bead {} in column {}'.format(index, column))
        abacus.columns[column].ToggleUpper(index)
        showAbacus(abacus)

    # ToggleLower
    def toggleLowerTest(abacus, column, index):
        print('Toggling lower bead {} in column {}'.format(index, column))
        abacus.columns[column].ToggleLower(index)
        showAbacus(abacus)

    toggleUpperTest(abacus, 1, 1)
    toggleUpperTest(abacus, 0, 0)
    toggleUpperTest(abacus, 0, 1)

    toggleLowerTest(abacus, 0, 2)
    toggleLowerTest(abacus, 1, 4)
    toggleLowerTest(abacus, 1, 2)
    toggleLowerTest(abacus, 0, 3)
