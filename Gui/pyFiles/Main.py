from kivy.lang import Builder

from Gui.pyFiles.WindowManager import WindowManager
from kivy.app import App


class MyApp(App):
    def build(self):
        windowManager = WindowManager()
        # change screens in code
        Builder.load_file("Gui/kvFiles/main.kv")
        windowManager.initalize()
        return windowManager