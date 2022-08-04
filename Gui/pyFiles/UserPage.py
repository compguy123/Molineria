from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from Gui.pyFiles.state_store import get_state
from data.specifications import GetAllUsersMedicationDetails
from data.unit_of_work import MolineriaUnitOfWork
from Gui.pyFiles.UserRV import UserRV


class UserPage(Screen, RecycleView):
    userName = ObjectProperty()
    userDOB = ObjectProperty()

    def on_enter(self, *args):
        state = get_state()
        id = state.current_user.id
        name = state.current_user.name
        date_of_birth = state.current_user.date_of_birth
        date_of_birth = date_of_birth if date_of_birth else ""
        self.userName.text = name
        self.userDOB.text = date_of_birth

        # show user its medication
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            spec = GetAllUsersMedicationDetails(unit_of_work, id)
            user_medications = spec.execute()
            if user_medications:
                self.data = [{"text": str(u.medication.name)} for u in user_medications]
                user_meds: UserRV = self.ids.userMeds
                user_meds.refreshMeds(self.data)
