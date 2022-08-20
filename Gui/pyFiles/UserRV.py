import logging
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from Gui.pyFiles.BaseRecyclerViewer import BaseRecyclerViewer
from Gui.pyFiles.navigation_manager import NavigationManager
from Gui.pyFiles.state_store import get_state
from data.specifications import GetAllUsersMedicationDetailsWithIntakes
from data.unit_of_work import MolineriaUnitOfWork

logger = logging.getLogger().getChild(__name__)


class UserRV(BaseRecyclerViewer):
    def refresh_data(self):
        id = get_state().current_user.id
        logger.info(f"<{__class__.__name__}> refreshing list")
        # show user its medication
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            spec = GetAllUsersMedicationDetailsWithIntakes(unit_of_work, id)
            user_medications = spec.execute()
            if user_medications:
                self.data = [
                    {
                        "user_medication_id": d.user_medication.id,
                        "text": f"{d.medication.name} - {d.user_medication_intake.next_intake_as_target().remaining_short_humanized}",
                    }
                    for [d, tail_intakes] in user_medications
                ]

    @property
    def rv_data(self):
        return self.data


class UserMedicationNavButton(Button):
    user: UserRV = ObjectProperty(None)
    user_medication_id: int

    def on_release(self, **kwargs):
        super().on_release()
        state = get_state()
        state.selected_user_medication_id = self.user_medication_id
        NavigationManager.go_left("Intake")
