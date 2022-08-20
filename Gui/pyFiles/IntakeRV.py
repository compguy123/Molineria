import logging
from kivy.uix.recycleview import RecycleView
from Gui.pyFiles.BaseRecyclerViewer import BaseRecyclerViewer
from Gui.pyFiles.state_store import get_state
from data.models import UserMedicationDetailWithIntakeDTO
from data.specifications import GetAllUsersMedicationDetailsWithIntakes
from data.unit_of_work import MolineriaUnitOfWork
from util.iterable import find

logger = logging.getLogger().getChild(__name__)


class IntakeRV(BaseRecyclerViewer):
    def refresh_data(self):
        state = get_state()
        id = state.current_user.id
        user_med_id = state.selected_user_medication_id

        logger.info(f"<{__class__.__name__}> refreshing list")
        # show user its medication
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            spec = GetAllUsersMedicationDetailsWithIntakes(unit_of_work, id)
            user_medications = spec.execute()
            target_user_med = find(
                lambda um: um[0].user_medication.id == user_med_id, user_medications
            )

            if target_user_med:
                user_med, intakes = target_user_med
                self.user_med = user_med
                self.data = [
                    {
                        "text": f"{intake.amount_in_milligrams}mg(s) - {intake.next_intake_as_target().remaining_short_humanized}"
                    }
                    for intake in intakes
                    if intake.id
                ]

    @property
    def rv_data(self):
        return self.data
