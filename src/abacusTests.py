
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

def testNum(func):
    def inner_func(*args, **kwargs):
        testNum.test += 1
        print('========== TEST #{} =========='.format(testNum.test))
        return func(*args, **kwargs)
    return inner_func

# SetValue
@testNum
def setValueTest(abacus, value):
    print("Changing value to {}".format(value))
    abacus.SetValue(value)
    showAbacus(abacus)
    print()

# GetValue
@testNum
def getValueTest(abacus):
    print('Value of abacus is {}'.format(abacus.GetValue()))
    showAbacus(abacus)
    print()

# ToggleUpper
@testNum
def toggleUpperTest(abacus, column, index):
    print('Toggling upper bead {} in column {}'.format(index, column))
    print('   Original')
    showAbacus(abacus)
    abacus.columns[column].ToggleUpper(index)
    print('   After')
    showAbacus(abacus)
    print()

# ToggleLower
@testNum
def toggleLowerTest(abacus, column, index):
    print('Toggling lower bead {} in column {}'.format(index, column))
    print('   Original')
    showAbacus(abacus)
    abacus.columns[column].ToggleLower(index)
    print('   After')
    showAbacus(abacus)
    print()
print('\n')    # Create and display an abacus

@testNum
def beadStateTest(abacus):
    print("Bead State Test")
    showAbacus(abacus)
    print("Abacus Value: {}\n".format(abacus.GetValue()))
    print("Lower Columns:")
    for index, column in enumerate(abacus.columns):
        print("\nColumn: {}".format(index))
        expectedResult = column.GetValue()%5
        resultTally = 0
        print("Expected Value: {}".format(expectedResult))
        for i in range(5):
            result = column.GetLowerBeadState(i)
            print(i, result)
            if result:
                resultTally += 1
    print("Test Passed: {}\n".format(resultTally == expectedResult))
    print("Upper Columns:")
    for index, column in enumerate(abacus.columns):
        print("\nColumn: {}".format(index))
        expectedResult = column.GetValue()//5
        resultTally = 0
        print("Expected Value: {}".format(expectedResult))
        for i in range(5):
            result = column.GetUpperBeadState(i)
            print(i, result)
            if result:
                resultTally += 1
        print("Test Passed: {}".format(resultTally == expectedResult))


if(__name__ == '__main__'):

    abacus = Abacus(0, 3)
    testNum.test = 0
    
    setValueTest(abacus, 234)       # 1
    getValueTest(abacus)            # 2

    setValueTest(abacus, 700)       # 3
    getValueTest(abacus)            # 4

    setValueTest(abacus, 5)         # 5
    getValueTest(abacus)            # 6

    setValueTest(abacus, 999)       # 7
    getValueTest(abacus)            # 8

    setValueTest(abacus, 549)       # 9
    getValueTest(abacus)            # 10

    setValueTest(abacus, 0)         # 11
    getValueTest(abacus)            # 12

    toggleUpperTest(abacus, 1, 1)   # 13
    toggleUpperTest(abacus, 1, 1)   # 14
    toggleUpperTest(abacus, 0, 0)   # 15
    toggleUpperTest(abacus, 0, 1)   # 16
    toggleUpperTest(abacus, 0, 0)   # 17

    toggleLowerTest(abacus, 0, 2)   # 18
    toggleLowerTest(abacus, 1, 4)   # 19
    toggleLowerTest(abacus, 1, 2)   # 20
    toggleLowerTest(abacus, 0, 3)   # 21
    toggleLowerTest(abacus, 0, 3)   # 22
    toggleLowerTest(abacus, 2, 4)   # 23
    toggleLowerTest(abacus, 2, 0)   # 24

    abacus.SetValue(0)
    toggleLowerTest(abacus, 0, 1)   # 25
    toggleLowerTest(abacus, 0, 0)   # 26

    beadStateTest(abacus)           # 27