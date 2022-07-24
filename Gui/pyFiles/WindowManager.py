from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager

from Gui.pyFiles.Homepage import Homepage
from Gui.pyFiles.InsertUser import InsertUser
from Gui.pyFiles.ShowUser import ShowUser


class WindowManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def initalize(self):
        screens = {Homepage(name="Homepage"), InsertUser(name="InsertUser"),
                   ShowUser(name="ShowUser")}
        for screen in screens:
            self.add_widget(screen)

# load kv file

# screen manager
