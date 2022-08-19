import logging
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen

from Gui.pyFiles.BaseScreen import BaseScreen
from Gui.pyFiles.PopupUtil import PopupUtil
from Gui.pyFiles.state_store import get_state

from data.exceptions import UniqueConstraintException
from data.models import Medication, UserMedication
from data.unit_of_work import MolineriaUnitOfWork
from util.string import is_null_or_whitespace, is_int, is_float, is_date

logger = logging.getLogger().getChild(__name__)


class AddMedication(BaseScreen):
    # mandatory
    medname: TextInput = ObjectProperty()
    rxnumber: TextInput = ObjectProperty()
    quantity: TextInput = ObjectProperty()
    weight_pill: TextInput = ObjectProperty()

    #optional
    filled_on: TextInput = ObjectProperty()
    discarded_on: TextInput = ObjectProperty()
    refills: TextInput = ObjectProperty()
    total_weight: TextInput = ObjectProperty()

    def checkValid(self):
        if is_null_or_whitespace(self.medname.text):
            PopupUtil.error("Med Name is required")
            return False
        if is_null_or_whitespace(self.rxnumber.text):
            PopupUtil.error("Rx num is required")
            return False
        if is_null_or_whitespace(self.quantity.text):
            PopupUtil.error("Quantity required")
            return False
        if not is_int(self.quantity.text):
            PopupUtil.error("Quantity should be a number")
            return False
        if is_null_or_whitespace(self.weight_pill.text):
            PopupUtil.error("Weight of pill is required")
            return False
        if not is_float(self.weight_pill.text):
            PopupUtil.error("Weight of pill should be a number")
            return False
        if self.refills.text and not is_int(self.refills.text):
            PopupUtil.error("Refills should be a number")
            return False
        if self.total_weight.text and not is_float(self.total_weight.text):
            PopupUtil.error("Total Weight  should be a number")
            return False
        if self.filled_on.text and not is_date(self.filled_on.text):
            PopupUtil.error("Filled on must be a valid date (YYYY-MM-DD")
            return False
        if self.discarded_on.text and not is_date(self.discarded_on.text):
            PopupUtil.error("Discarded on must be a valid date (YYYY-MM-DD")
            return False

        return True



    def onCreate(self):
        state = get_state()
        id = state.current_user.id

        if self.checkValid():
            unit_of_work = MolineriaUnitOfWork("data/molineria.db")
            with unit_of_work:
                medication = Medication(
                    name=self.medname.text,
                )
                created_med = False
                try:
                    inserted_med = unit_of_work.medication_repo.create(medication)
                    logger.debug(f"INSERTED MED: {inserted_med}")
                    user_medication = UserMedication(
                        user_id=id,
                        medication_id=inserted_med.id,
                        rx_number=self.rxnumber.text,
                        quantity=self.quantity.text
                    )
                    inserted_user_med = unit_of_work.user_medication_repo.create(
                        user_medication
                    )
                    logger.debug(f"INSERTED USER MED: {inserted_user_med}")
                    self.reset()
                    created_med = True
                except UniqueConstraintException:
                    PopupUtil.error("Duplicate Medication")
                    created_med = False
                return created_med
        else:
            return False


    def reset(self):
        self.medname.text = ""
        self.rxnumber.text = ""
