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