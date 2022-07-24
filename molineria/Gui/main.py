from kivy.properties import ObjectProperty
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
<<<<<<<< HEAD:Gui/pyFiles/InsertUser.py
========
from datetime import date, datetime

from data.models import User
from data.unit_of_work import MolineriaUnitOfWork


class Homepage(Screen):
    pass
>>>>>>>> dev:molineria/Gui/main.py


class InsertUser(Screen):
    userName = ObjectProperty(None)
    comments = ObjectProperty(None)
    dob = ObjectProperty(None)

    def createUser(self):
        unit_of_work = MolineriaUnitOfWork("molineria/data/molineria.db")
        with unit_of_work:
            # check user variables are valid
            if self.userName.text != "" and self.validateDate():
                parsed_date = datetime.strptime(self.dob.text, "%Y-%m-%d")
                user = User(
                    name=self.userName.text,
                    date_of_birth=parsed_date.date(),
                    comment=self.comments.text,
                )
                inserted_user = unit_of_work.user_repo.create(user)
                print(f"INSERTED USER: {inserted_user}")

<<<<<<<< HEAD:Gui/pyFiles/InsertUser.py
            self.reset()
        else:
            invalidUser()
========
                self.reset()
                windowManager.current = "ShowUser"
            else:
                invalidUser()
>>>>>>>> dev:molineria/Gui/main.py

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


<<<<<<<< HEAD:Gui/pyFiles/InsertUser.py
========
class ShowUser(Screen):
    pass


class WindowManager(ScreenManager):
    pass


# load kv file
kv = Builder.load_file("Gui/my.kv")

# screen manager
windowManager = WindowManager()

# change screens in code
screens = {
    Homepage(name="Homepage"),
    InsertUser(name="InsertUser"),
    ShowUser(name="ShowUser"),
}
for screen in screens:
    windowManager.add_widget(screen)


>>>>>>>> dev:molineria/Gui/main.py
# create pipup
def invalidUser():
    pop = Popup(
        title="Error", content=Label(text="Invalid name or date."), size_hint=(0.4, 0.4)
    )
    pop.open()
