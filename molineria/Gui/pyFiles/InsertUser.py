from kivy.properties import ObjectProperty
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from datetime import date, datetime

from data.models import User
from data.unit_of_work import MolineriaUnitOfWork


class InsertUser(Screen):
    userName = ObjectProperty(None)
    comments = ObjectProperty(None)
    dob = ObjectProperty(None)

    def createUser(self):
        # check user variables are valid
        if self.userName.text != "" and self.validateDate():
            unit_of_work = MolineriaUnitOfWork("molineria/data/molineria.db")
            with unit_of_work:
                parsed_date = datetime.strptime(self.dob.text, "%Y-%m-%d")
                user = User(
                    name=self.userName.text,
                    date_of_birth=parsed_date.date(),
                    comment=self.comments.text,
                )
                inserted_user = unit_of_work.user_repo.create(user)
                print(f"INSERTED USER: {inserted_user}")
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
            datetime.strptime(self.dob.text, "%Y-%m-%d")
            return True
        except ValueError as ex:
            return False


# create pipup
def invalidUser():
    pop = Popup(
        title="Error", content=Label(text="Invalid name or date."), size_hint=(0.4, 0.4)
    )
    pop.open()
