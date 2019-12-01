class User:
    def __init__(self, idNum: str, password: str, name: str):
        self.idNum = idNum
        self.password = password
        self.name = name
        return

    def GetID(self) -> str:
        return self.idNum


class Teacher(User):
    def __init__(self):
        return


class Student(User):
    def __init__(self):
        return


class Admin(User):
    def __init__(self):
        return


class Class:
    def __init__(self, idNum: str, name: str):
        self.idNum = idNum
        self.name = name
        self.listOfStudents = [Student]
        self.teacher = None
        return

    def GetID(self):
        return self.idNum

    def GetTeacher(self) -> Teacher:
        if self.teacher is not None:
            return self.teacher
        else:
            return None

    def SetTeacher(self, newTeacher: Teacher):
        self.classTeacher = newTeacher
        return

    def AddStudent(self, newStudent: Student):
        self.listOfStudents.append(newStudent)

    def RemoveStudent(self, studentID: str = None, newStudent: Student = None) -> bool:
        removeStudentIndex = None
        if newStudent is None and studentID is None:
            return False
        if newStudent is not None:
            studentID = newStudent.idNum
        for index, oneStudent in enumerate(self.listOfStudents):
            if oneStudent.idNum == studentID:
                removeStudentIndex = index
        if removeStudentIndex is not None:
            del self.listOfStudents[removeStudentIndex]
            return True
        else:
            return False
