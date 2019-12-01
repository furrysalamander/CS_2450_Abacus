
from abacus import *


def showAbacus(abacus):
    for col in abacus.columns:
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
        showAbacus(abacus)
    
    # GetValue
    def getValueTest(abacus):
        print('Value of abacus is {}'.format(abacus.getValue()))
        showAbacus(abacus)
    
    setValueTest(abacus, 234)
    getValueTest(abacus)

    setValueTest(abacus, 700)
    getValueTest(abacus)

    setValueTest(abacus, 555)
    getValueTest()

    setValueTest(abacus, 999)
    getValueTest(abacus)

    setValueTest(abacus, 549)
    getValueTest(abacus)
