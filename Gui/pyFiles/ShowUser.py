from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from Gui.pyFiles.RV import RV


class ShowUser(Screen):
    # initalize recycler vierer
    rv = RV()