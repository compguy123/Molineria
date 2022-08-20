import logging
from datetime import time
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from Gui.pyFiles.BaseScreen import BaseScreen
from Gui.pyFiles.IntakeRV import IntakeRV
from Gui.pyFiles.PopupUtil import PopupUtil
from Gui.pyFiles.state_store import get_state

from kivy.factory import Factory
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from data.exceptions import MolineriaDataException
from data.models import DayOfWeek, UserMedicationIntake

from data.unit_of_work import MolineriaUnitOfWork
from util.string import is_float, is_iso_time, is_null_or_whitespace

logger = logging.getLogger().getChild(__name__)


class MultiSelectSpinner(Button):
    """Widget allowing to select multiple text options."""

    dropdown: DropDown = ObjectProperty(None)
    """(internal) DropDown used with MultiSelectSpinner."""

    values: list[str] = ListProperty([])
    """Values to choose from."""

    selected_values: list[str] = ListProperty([])
    """List of values selected by the user."""

    def __init__(self, **kwargs):
        self.bind(dropdown=self.update_dropdown)  # type: ignore
        self.bind(values=self.update_dropdown)  # type: ignore
        super(MultiSelectSpinner, self).__init__(**kwargs)
        self.bind(on_release=self.toggle_dropdown)  # type: ignore

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
                b = Factory.MultiSelectOption(text=value)  # type: ignore
                b.bind(state=self.select_value)  # type: ignore
                self.dropdown.add_widget(b)

    def select_value(self, instance, value):
        if value == "down":
            if instance.text not in self.selected_values:
                self.selected_values.append(instance.text)
        else:
            if instance.text in self.selected_values:
                self.selected_values.remove(instance.text)

    def on_selected_values(self, instance, value):
        if value:
            self.text = ", ".join(value)
        else:
            self.text = ""


class Intake(BaseScreen):
    time: TextInput = ObjectProperty(None)
    amount: TextInput = ObjectProperty(None)
    days: MultiSelectSpinner = ObjectProperty(None)

    def on_enter(self, *args):
        state = get_state()

        def set_title(*args, **kwargs):
            unit_of_work = MolineriaUnitOfWork("data/molineria.db")
            with unit_of_work:
                user_med = unit_of_work.user_medication_repo.get(
                    state.selected_user_medication_id
                )
                med_name = ""
                if user_med:
                    med = unit_of_work.medication_repo.get(user_med.medication_id)
                    med_name = med.name if med else ""
                state.app_title += f" - {med_name}"

        Clock.schedule_once(set_title, 0.1)
        return super().on_enter(*args)

    def is_inputs_valid(self):
        if is_null_or_whitespace(self.time.text):
            PopupUtil.error("time is required.")
            return False
        if is_null_or_whitespace(self.time.text):
            PopupUtil.error("time is required.")
            return False
        if is_null_or_whitespace(self.amount.text):
            PopupUtil.error("amount is required.")
            return False
        if not is_float(self.amount.text):
            PopupUtil.error("amount must be a number.")
            return False
        if not is_iso_time(self.time.text):
            PopupUtil.error("time must be in iso format (24hr:min:sec).")
            return False
        if not any(self.days.selected_values):
            PopupUtil.error("You must pick at least one day of week.")
            return False
        return True

    def create(self):
        state = get_state()
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            intake = UserMedicationIntake(
                user_medication_id=state.selected_user_medication_id,
                time=self.time.text,
                amount_in_milligrams=float(self.amount.text),
            )
            days_of_week = list(map(DayOfWeek.parse, self.days.selected_values))
            for d in days_of_week:
                intake.try_add_day_of_week(d)

            try:
                inserted_intake = unit_of_work.user_medication_intake_repo.create(
                    intake
                )
                logger.debug(f"INSERTED INTAKE: {inserted_intake}")
                self.reset_inputs()
            except MolineriaDataException as err:
                logger.error(f"Failed to create intake: {err}")

    def reset_inputs(self):
        self.time.text = ""
        self.amount.text = ""
        self.days.selected_values = []
