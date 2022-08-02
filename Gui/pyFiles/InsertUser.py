from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from datetime import date, datetime

from data.models import User
from data.unit_of_work import MolineriaUnitOfWork

from util.string_util import is_null_or_whitespace


class InsertUser(Screen):
    userName = ObjectProperty(None)
    comments = ObjectProperty(None)
    dob = ObjectProperty(None)

    def createUser(self):
        # check user variables are valid
        if self.userName.text != "" and self.validateDate():
            unit_of_work = MolineriaUnitOfWork("data/molineria.db")
            with unit_of_work:
                parsed_date: date | None = None
                if not self.dob or not is_null_or_whitespace(self.dob.text):
                    parsed_date = datetime.strptime(self.dob.text, "%Y-%m-%d").date()

                user = User(
                    name=self.userName.text,
                    date_of_birth=parsed_date,
                    comment=self.comments.text,
                )
                inserted_user = unit_of_work.user_repo.create(user)
                print(f"INSERTED USER: {inserted_user}")
                self.reset()
                return True
        else:
            self.invalidUser()
            return False

    # reset user variable
    def reset(self):
        self.userName.text = ""
        self.comments.text = ""
        self.dob.text = ""

    # check date
    def validateDate(self):
        if not self.dob or is_null_or_whitespace(self.dob.text):
            return True
        try:
            datetime.strptime(self.dob.text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # create pipup
    def invalidUser(self):
        self.pop = Popup(
            title="Error", content=Label(text="Invalid name or date."), size_hint=(0.4, 0.4), auto_dismiss=True
        )

        self.pop.open()

