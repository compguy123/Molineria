from datetime import date


# This is a person Object. The takes in the name and age and calcualtes the  age

class Person:
    name = ""
    born = None
    age: int = 0

    def __init__(self, name: str, born: date):
        self.name = name
        self.born = born
        today = date.today()
        # calculate age of person
        self.age = today.year - self.born.year - ((today.month, today.day) < (self.born.month, self.born.day))
