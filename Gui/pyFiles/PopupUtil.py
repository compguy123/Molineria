from kivy.uix.label import Label
from kivy.uix.popup import Popup
from abc import ABC


class PopupUtil(ABC):
    @staticmethod
    def error(text):
        pop = Popup(
            title="Error",
            content=Label(text=text),
            size_hint=(0.4, 0.4),
            auto_dismiss=True,
        )
        pop.open()
