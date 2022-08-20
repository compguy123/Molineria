import logging
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager
from Gui.pyFiles.Homepage import Homepage
from Gui.pyFiles.InsertUser import InsertUser
from Gui.pyFiles.ShowUser import ShowUser
from Gui.pyFiles.UserPage import UserPage
from Gui.pyFiles.AddMedication import AddMedication
from Gui.pyFiles.Intake import Intake

logger = logging.getLogger().getChild(__name__)


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initalize(self):
        screens: list[Widget] = [
            Homepage(name="Homepage"),
            InsertUser(name="InsertUser"),
            ShowUser(name="ShowUser"),
            UserPage(name="UserPage"),
            AddMedication(name="AddMedication"),
            Intake(name="Intake"),
        ]
        for screen in screens:
            self.add_widget(screen)
        self.current = "Homepage"
