import logging
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock, ClockEvent
from Gui.pyFiles.state_store import get_state
from Gui.pyFiles.UserRV import UserRV
from data.specifications import (
    GetAllUsersMedicationDetails,
    GetAllUsersMedicationDetailsWithIntakes,
)
from data.unit_of_work import MolineriaUnitOfWork

logger = logging.getLogger().getChild(__name__)


class UserPage(Screen, RecycleView):
    userName: TextInput = ObjectProperty()
    userDOB: TextInput = ObjectProperty()

    def refresh_list(self, id: int):
        logger.info(f"<{__class__.__name__}> refreshing list")
        # show user its medication
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            spec = GetAllUsersMedicationDetailsWithIntakes(unit_of_work, id)
            user_medications = spec.execute()
            if user_medications:
                self.data = [
                    {
                        "text": f"{d.medication.name} - {d.user_medication_intake.next_intake_as_target().remaining_short_humanized}"
                    }
                    for [d, tail_intakes] in user_medications
                ]
                user_meds: UserRV = self.ids.userMeds
                user_meds.refreshMeds(self.data)

    def on_pre_enter(self, *args):
        state = get_state()
        id = state.current_user.id
        name = state.current_user.name
        date_of_birth = state.current_user.date_of_birth
        date_of_birth = date_of_birth if date_of_birth else ""
        self.userName.text = name
        self.userDOB.text = date_of_birth

        self.refresh_list(id)
        self.refresh_list_event: ClockEvent = Clock.schedule_interval(
            lambda _: self.refresh_list(id), 0.5
        )

    def on_pre_leave(self):
        if self.refresh_list_event and callable(self.refresh_list_event.cancel):
            self.refresh_list_event.cancel()
