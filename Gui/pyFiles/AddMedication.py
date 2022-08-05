from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from Gui.pyFiles.state_store import get_state

from data.exceptions import UniqueConstraintException
from data.models import Medication, UserMedication
from data.unit_of_work import MolineriaUnitOfWork
from util.string import is_null_or_whitespace


class AddMedication(Screen):
    medname: TextInput = ObjectProperty()
    rxnumber: TextInput = ObjectProperty()


    def onCreate(self):
        state = get_state()
        id = state.current_user.id
        if not is_null_or_whitespace(self.medname.text):
            unit_of_work = MolineriaUnitOfWork("data/molineria.db")
            with unit_of_work:
                medication = Medication(
                    name=self.medname.text,
                )
                created_med = False
                try:
                    inserted_med = unit_of_work.medication_repo.create(medication)
                    print(f"INSERTED MED: {inserted_med}")
                    user_medication = UserMedication(
                        user_id=id,
                        medication_id=inserted_med.id,
                        rx_number=self.rxnumber.text,
                    )
                    inserted_user_med = unit_of_work.user_medication_repo.create(
                        user_medication
                    )
                    print(f"INSERTED USER MED: {inserted_user_med}")
                    self.reset()
                    created_med = True
                except UniqueConstraintException:
                    self.invalidUser("Duplicate Medication")
                    created_med = False
                return created_med
        else:
            self.invalidUser("Invalid Name or Date")
            return False

        # create pipup

    def invalidUser(self, text):
        self.pop = Popup(
            title="Error",
            content=Label(text=text),
            size_hint=(0.4, 0.4),
            auto_dismiss=True,
        )

        self.pop.open()

    def reset(self):
        self.medname.text = ""
