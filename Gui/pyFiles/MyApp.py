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

    def go(self, page: str, dir: str) -> None:
        app = self
        if app and app.root:
            screen_manager = app.root
            screen_manager.transition.direction = dir  # type: ignore
            screen_manager.current = page  # type: ignore

    def go_right(self, page: str) -> None:
        app = self
        if app and app.root:
            screen_manager = app.root
            screen_manager.transition.direction = "right"  # type: ignore
            screen_manager.current = page  # type: ignore

    def go_left(self, page: str) -> None:
        app = self
        if app and app.root:
            screen_manager = app.root
            screen_manager.transition.direction = "left"  # type: ignore
            screen_manager.current = page  # type: ignore
