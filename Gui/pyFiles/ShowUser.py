from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from Gui.pyFiles.RV import RV


class ShowUser(Screen):

    def on_enter(self, *args):
        self.ids.userList.refreshList()
