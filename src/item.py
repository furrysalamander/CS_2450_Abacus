from datetime import datetime

class Question:
    # TODO: Honestly, this whole constructor needs to be revisited
    def __init__(
            self,
            idNum: str,
            abacusColumns: int,
            # TODO: I need an explanation for what these two are for
            # These are here to give questions the ability to use different abacus bases if the want
            # We can remove them if we are hardcoding a 5-2 abacus
            abacusNumUpper: int,
            abacusNumLower: int,
            goal: int,
            prompt: str,
            pointValue: int,
            dispAbacus: bool,
            enableAbacus: bool
            ):
        self.idNum = idNum
        self.abacusColumns = abacusColumns
        self.abacusNumUpper = abacusNumUpper
        self.abacusNumLower = abacusNumLower
        self.goal = goal
        self.prompt = prompt
        self.pointValue = pointValue
        self.dispAbacus = dispAbacus
        self.enableAbacus = enableAbacus
        pass
    def GetID(self) -> str:
        """ Returns the question's unique ID
        """
        return self.idNum
    def SetAbacusColumns(self, count: int):
        """ Sets the number of columns the question will have in it's Abacus
        """
        pass
        # We should probably remove these two now that I think about it
    def SetAbacusUpperBeads(self, count: int):
        pass
    def SetAbacusLowerBeads(self, count: int):
        pass
    def Grade(self) -> int:
        pass

class MultipleChoice_Q(Question):
    def __init__(self, options: [str] = [str], answer_index: int = None):
        self.options = options
        self.answer_index = answer_index
    def AddOption(self, option: str) -> int:
        self.options.append(option)
        return len(self.options) - 1
    def ClearOptions(self):
        self.options = [str]
        self.answer_index = None
    def SetAnswer(self, index: int) -> bool:
        if 0 <= index < len(self.options):
            self.answer_index = index
            return True
        else:
            return False
    def ClearAnswer(self):
        self.answer_index = None

class Arithmetic_Q(Question):
    def __init__(self, startValue: int = None, endValue: int = None, steps: [int] = [int]):
        self.startValue = startValue
        self.endValue = endValue
        self.steps = steps
    def SetStartValue(self, value: int):
        self.startValue = value
    def SetEndvalue(self, value: int):
        self.endValue = value
    def GetNumSteps(self):
        return len(self.steps)
    def GetStep(self, step_index: int) -> int:
        return self.steps[step_index]
    def CalculateSteps(self):
        pass
    
class Interpret_Q(Question):
    pass
class Match_Q(Question):
    pass

class Assignment:
    def __init__(
            self, 
            idNum: str, 
            title: str, 
            dueDate: datetime = None, 
            description: str = None, 
            showAnswers: bool = False, 
            fastGrading: bool = False,
            listOfQuestions: list = []
            ):
        self.idNum = idNum
        self.title = title
        self.dueDate = dueDate
        self.description = description
        self.showAnswers = showAnswers
        self.fastGrading = fastGrading
        self.listOfQuestions = listOfQuestions
        return

    def GetID(self) -> str:
        return self.idNum
    def GetDueDate(self) -> datetime:
        return self.dueDate
    def SetDueDate(self, newDueDate: datetime):
        self.dueDate = newDueDate
    def SetShowAnswers(self, enabled: bool):
        self.showAnswers = enabled
    def SetFastGrading(self, enabled: bool):
        self.fastGrading = enabled

    def AddQuestion(self, newQuestion: Question):
        self.listOfQuestions.append(newQuestion)
    def RemoveQuestion(self, questionID: str = None, newQuestion: Question = None) -> bool:
        pass

class Test(Assignment):
    pass

