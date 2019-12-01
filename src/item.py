from datetime import datetime


class Question:
    # TODO: Honestly, this whole constructor needs to be revisited
    def __init__(
        self,
        idNum: str,
        goal: int,
        prompt: str,
        pointValue: int,
        dispAbacus: bool,
        enableAbacus: bool,
        abacusColumns: int = 7,
    ):
        self.idNum = idNum
        self.abacusColumns = abacusColumns
        self.goal = goal
        self.prompt = prompt
        self.pointValue = pointValue
        self.dispAbacus = dispAbacus
        self.enableAbacus = enableAbacus

    def GetID(self) -> str:
        """ Returns the question's unique ID
        """
        return self.idNum

    def SetAbacusColumns(self, count: int):
        """ Sets the number of columns the question will have in it's Abacus
        """
        self.abacusColumns = count

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
        self.options.clear()
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
    def __init__(
        self, startValue: int = None, endValue: int = None, steps: [int] = [int]
    ):
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
        listOfQuestions: list = [],
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

    def RemoveQuestion(
        self, questionID: str = None, newQuestion: Question = None
    ) -> bool:
        removeQuestionIndex = None
        if newQuestion is None and questionID is None:
            return False
        if newQuestion is not None:
            questionID = newQuestion.idNum
        for index, oneQuestion in enumerate(self.listOfQuestions):
            if oneQuestion.idNum == questionID:
                removeQuestionIndex = index
        if removeQuestionIndex is not None:
            del self.listOfQuestions[removeQuestionIndex]
            return True
        else:
            return False


class Test(Assignment):
    pass

