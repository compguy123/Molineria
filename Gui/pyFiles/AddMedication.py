import logging
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from Gui.pyFiles.BaseScreen import BaseScreen
from Gui.pyFiles.PopupUtil import PopupUtil
from Gui.pyFiles.state_store import get_state
from Gui.pyFiles.navigation_manager import NavigationManager
from data.exceptions import UniqueConstraintException
from data.models import Medication, UserMedication
from data.specifications import GetAllUsersMedicationDetails
from data.unit_of_work import MolineriaUnitOfWork
from util.iterable import find
from util.string import is_null_or_whitespace, is_int, is_float, is_date, to_date

logger = logging.getLogger().getChild(__name__)


class AddMedication(BaseScreen):
    # mandatory
    medname: TextInput = ObjectProperty()
    rxnumber: TextInput = ObjectProperty()
    quantity: TextInput = ObjectProperty()
    weight_pill: TextInput = ObjectProperty()
    label: TextInput = ObjectProperty()

    # optional
    filled_on: TextInput = ObjectProperty()
    discarded_on: TextInput = ObjectProperty()
    refills: TextInput = ObjectProperty()
    total_weight: TextInput = ObjectProperty()

    # delete button
    delete_button: Button = ObjectProperty()
    # layout
    layout: FloatLayout = ObjectProperty()

    def is_edit_mode(self):
        state = get_state()
        return not state.selected_user_medication_id is 0

    def on_enter(self, *args):
        state = get_state()
        check_delete_button = False
        if self.is_edit_mode():
            self.delete_button.pos_hint = {"x": .05, "top": .2}
            unit_of_work = MolineriaUnitOfWork("data/molineria.db")
            with unit_of_work:
                user_meds = GetAllUsersMedicationDetails(unit_of_work, state.current_user.id).execute()
                user_med = find(lambda u: u.user_medication.id == state.selected_user_medication_id, user_meds)
                self.medname.text = user_med.medication.name
                self.rxnumber.text = user_med.user_medication.rx_number
                self.quantity.text = str(user_med.user_medication.quantity)
                self.weight_pill.text = str(user_med.user_medication.weight_in_milligrams)
                self.label.text = "Edit Medication"
                self.total_weight.text= str(user_med.user_medication.total_weight_in_milligrams)

                if user_med.user_medication.remaining_refills:
                    self.refills.text = str(user_med.user_medication.remaining_refills)

                if user_med.user_medication.filled_on:
                    self.filled_on.text = to_date(user_med.user_medication.filled_on).strftime("%Y-%m-%d")

                if user_med.user_medication.discard_on:
                    self.discarded_on.text = to_date(user_med.user_medication.discard_on).strftime("%Y-%m-%d")

                if user_med.user_medication.total_weight_in_milligrams:
                    self.total_weight.text = str(user_med.user_medication.total_weight_in_milligrams)
        else:
            self.label.text = "Add Medication"
            self.delete_button.pos_hint = {"x": -9, "top": -1}

    def delete_med(self):
        if not self.is_edit_mode():
            return
        state = get_state()
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            unit_of_work.user_medication_repo.delete(state.selected_user_medication_id)
        state.selected_user_medication_id = 0
        NavigationManager.go_right("UserPage")

    def on_leave(self, *args):
        self.reset()

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

    def try_get_or_create_medication(
            self, unit_of_work: MolineriaUnitOfWork
    ) -> tuple[bool, Medication]:
        state = get_state()
        current_user_id = state.current_user.id
        all_meds = unit_of_work.medication_repo.get_all()
        existing_meds: list[Medication] = list(
            filter(lambda m: m.name == self.medname.text, all_meds)
        )
        existing_med: Medication | None = None
        if any(existing_meds):
            existing_med = existing_meds[0]

        medication: Medication
        if existing_med:
            if self.is_edit_mode():
                return True, existing_med
            medication = existing_med
            all_user_meds = unit_of_work.user_medication_repo.get_all()
            my_user_meds = list(
                filter(
                    lambda um: um.user_id == current_user_id,
                    all_user_meds,
                )
            )
            existing_user_meds: list[UserMedication] = list(
                filter(
                    lambda um: um.medication_id == medication.id,
                    my_user_meds,
                )
            )
            if any(existing_user_meds):
                PopupUtil.error(f"You already have '{existing_med.name}' medication")
                return False, medication
        else:
            medication = Medication(
                name=self.medname.text,
            )
            inserted_med = unit_of_work.medication_repo.create(medication)
            logger.debug(f"INSERTED MED: {inserted_med}")
            medication = inserted_med
        return True, medication

    def onCreate(self):
        state = get_state()
        user_id = state.current_user.id

        if self.checkValid():
            unit_of_work = MolineriaUnitOfWork("data/molineria.db")
            with unit_of_work:

                try:
                    is_successful, medication = self.try_get_or_create_medication(
                        unit_of_work
                    )
                    if not is_successful:
                        return False
                    quantity = (
                        int(self.quantity.text) if self.quantity.text else None
                    )
                    weight_in_milligrams = (
                        float(self.weight_pill.text) if self.weight_pill.text else None
                    )
                    total_weight_in_milligrams = (
                            weight_in_milligrams * quantity
                    )
                    filled_on = (
                        to_date(self.filled_on.text) if self.filled_on.text else None
                    )
                    discard_on = (
                        to_date(self.discarded_on.text)
                        if self.discarded_on.text
                        else None
                    )
                    remaining_refills = (
                        int(self.refills.text) if self.refills.text else None
                    )
                    if not self.is_edit_mode():
                        user_medication = UserMedication(
                            user_id=user_id,
                            medication_id=medication.id,
                            rx_number=self.rxnumber.text,
                            quantity=quantity,
                            weight_in_milligrams=weight_in_milligrams,
                            total_weight_in_milligrams=total_weight_in_milligrams,
                            filled_on=filled_on,
                            discard_on=discard_on,
                            remaining_refills=remaining_refills,
                        )
                        inserted_user_med = unit_of_work.user_medication_repo.create(
                            user_medication
                        )
                        logger.debug(f"INSERTED USER MED: {inserted_user_med}")
                        self.reset()

                        state.selected_user_medication_id = inserted_user_med.id

                        return True
                    else:
                        edit_med = unit_of_work.user_medication_repo.get(state.selected_user_medication_id)
                        edit_med.user_id = user_id
                        edit_med.medication_id = medication.id
                        edit_med.rx_number = self.rxnumber.text
                        edit_med.quantity = self.quantity.text
                        edit_med.weight_in_milligrams = weight_in_milligrams
                        edit_med.total_weight_in_milligrams = total_weight_in_milligrams
                        edit_med.filled_on = filled_on
                        edit_med.discard_on = discard_on
                        edit_med.remaining_refills = remaining_refills
                        unit_of_work.user_medication_repo.update(edit_med)
                        return True
                except UniqueConstraintException:
                    PopupUtil.error("Duplicate Medication")
                    return False
        else:
            return False

    def reset(self):
        self.medname.text = ""
        self.rxnumber.text = ""
        self.quantity.text = ""
        self.weight_pill.text = ""
        self.filled_on.text = ""
        self.discarded_on.text = ""
        self.refills.text = ""
        self.total_weight.text = ""
