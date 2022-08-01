from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.app import App


class UserPage(Screen):
    userName = ObjectProperty()

    def on_enter(self, *args):
        app = App.get_running_app()
        name = app.user_name
        self.userName.text = name
