import logging
from Gui.pyFiles.BaseRecyclerViewer import BaseRecyclerViewer
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.clock import Clock, ClockEvent

from Gui.pyFiles.BaseScreen import BaseScreen
from Gui.pyFiles.state_store import get_state
from Gui.pyFiles.UserRV import UserRV
from data.specifications import (
    GetAllUsersMedicationDetails,
    GetAllUsersMedicationDetailsWithIntakes,
)
from data.unit_of_work import MolineriaUnitOfWork

logger = logging.getLogger().getChild(__name__)


class UserPage(BaseScreen):
    userName: TextInput = ObjectProperty()
    userDOB: TextInput = ObjectProperty()

    def on_enter(self, *args):
        state = get_state()
        self.userName.text = state.current_user.name
        if state.current_user.date_of_birth:
            self.userDOB.text = state.current_user.date_of_birth
        else:
            self.userDOB.text = ""


