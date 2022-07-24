from kivy.properties import ObjectProperty
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class InsertUser(Screen):
    userName = ObjectProperty(None)
    comments = ObjectProperty(None)
    dob = ObjectProperty(None)

    def createUser(self):
        # check user variables are valid
        if self.userName.text != "" and self.validateDate():

            self.reset()
        else:
            invalidUser()

    # reset user variable
    def reset(self):
        self.userName.text = ""
        self.comments.text = ""
        self.dob.text = ""

    def homepage(self):
        pass

    # return to homepage

    # check date
    def validateDate(self):
        try:
            datetime.strptime(self.dob.text, '%Y-%m-%d')
            return True
        except ValueError as ex:
            return False


# create pipup
def invalidUser():
    pop = Popup(title='Error',
                content=Label(text='Invalid name or date.'),
                size_hint=(.4, .4))
    pop.open()
