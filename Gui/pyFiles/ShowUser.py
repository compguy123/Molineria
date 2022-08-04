from kivy.uix.screenmanager import Screen

from Gui.pyFiles.RV import RV


class ShowUser(Screen):
    def on_enter(self, *args):
        user_list: RV = self.ids.userList
        user_list.refreshList()
