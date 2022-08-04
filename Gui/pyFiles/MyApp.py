from kivy.app import App
from kivy.lang import Builder
from Gui.pyFiles.WindowManager import WindowManager
from Gui.pyFiles.state_store import StateStore


class MyApp(App):
    def build(self):
        windowManager = WindowManager()
        # change screens in code
        Builder.load_file("Gui/kvFiles/main.kv")
        windowManager.initalize()
        self.state = StateStore()
        return windowManager
