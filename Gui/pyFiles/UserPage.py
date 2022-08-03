from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.app import App

from kivy.uix.recycleview import RecycleView

from Gui.pyFiles.UserRV import UserRV
from data import unit_of_work
from data.unit_of_work import MolineriaUnitOfWork


class UserPage(Screen, RecycleView):
    userName = ObjectProperty()
    userDOB = ObjectProperty()

    def on_enter(self, *args):
        app = App.get_running_app()
        id = app.user_id
        name = app.user_name
        DOB  = app.user_DOB
        if DOB is None:
            DOB =""
        self.userName.text = name
        self.userDOB.text = DOB

        #show user its medication
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            users = unit_of_work.user_repo.get_all()
            if users:
                self.data = [{'text': str(u.name)} for u in users]
                self.ids.userMeds.refreshMeds(self.data)
