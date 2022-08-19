from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from Gui.pyFiles.BaseScreen import BaseScreen
from Gui.pyFiles.IntakeRV import IntakeRV
from Gui.pyFiles.state_store import get_state

from kivy.factory import Factory
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class Intake(BaseScreen):


    def on_enter(self, *args):
        state = get_state()
        IntakeRva = IntakeRV()
        mv = MultiSelectSpinner()
class MultiSelectSpinner(Button):
    """Widget allowing to select multiple text options."""

    dropdown = ObjectProperty(None)
    """(internal) DropDown used with MultiSelectSpinner."""

    values = ListProperty([])
    """Values to choose from."""

    selected_values = ListProperty([])
    """List of values selected by the user."""

    def __init__(self, **kwargs):
        self.bind(dropdown=self.update_dropdown)
        self.bind(values=self.update_dropdown)
        super(MultiSelectSpinner, self).__init__(**kwargs)
        self.bind(on_release=self.toggle_dropdown)

    def toggle_dropdown(self, *args):
        if self.dropdown.parent:
            self.dropdown.dismiss()
        else:
            self.dropdown.open(self)

    def update_dropdown(self, *args):
        if not self.dropdown:
            self.dropdown = DropDown()
        values = self.values
        if values:
            if self.dropdown.children:
                self.dropdown.clear_widgets()
            for value in values:
                b = Factory.MultiSelectOption(text=value)
                b.bind(state=self.select_value)
                self.dropdown.add_widget(b)

    def select_value(self, instance, value):
        if value == 'down':
            if instance.text not in self.selected_values:
                self.selected_values.append(instance.text)
        else:
            if instance.text in self.selected_values:
                self.selected_values.remove(instance.text)

    def on_selected_values(self, instance, value):
        if value:
            self.text = ', '.join(value)
        else:
            self.text = ''

