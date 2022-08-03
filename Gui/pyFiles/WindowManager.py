from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from Gui.pyFiles.Homepage import Homepage
from Gui.pyFiles.InsertUser import InsertUser
from Gui.pyFiles.ShowUser import ShowUser
from Gui.pyFiles.UserPage import UserPage
from Gui.pyFiles.AddMedication import AddMedication


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initalize(self):
        screens = {
            Homepage(name="Homepage"),
            InsertUser(name="InsertUser"),
            ShowUser(name="ShowUser"),
            UserPage(name="UserPage"),
            AddMedication(name="AddMedication")
        }
        for screen in screens:
            self.add_widget(screen)

        user_name = ""
        user_DOB = ""
        user_comments = ""
        user_id =0