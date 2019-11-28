
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
        pass

class Student(User):
    def __init__(self):
        pass

class Admin(User):
    def __init__(self):
        pass

class Class:
    def __init__(self, idNum: str, name: str):
        self.idNum = idNum
        self.name = name
        self.listOfStudents = list()
        return
    def GetID(self):
        return self.idNum
    def GetTeacher(self) -> Teacher:
        pass
    def SetTeacher(self, newTeacher: Teacher):
        self.classTeacher = newTeacher
        return
    def AddStudent(self, newStudent: Student) -> bool:
        pass
    def RemoveStudent(self, studentID: str = None, newStudent: Student = None) -> bool:
        pass