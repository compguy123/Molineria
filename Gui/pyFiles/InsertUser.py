import logging
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from datetime import date, datetime

from Gui.pyFiles.BaseScreen import BaseScreen
from Gui.pyFiles.PopupUtil import PopupUtil
from data.exceptions import UniqueConstraintException
from data.models import User
from data.unit_of_work import MolineriaUnitOfWork

from util.string import is_null_or_whitespace

logger = logging.getLogger().getChild(__name__)


class InsertUser(BaseScreen):
    userName: TextInput = ObjectProperty(None)
    comments: TextInput = ObjectProperty(None)
    dob: TextInput = ObjectProperty(None)

    def createUser(self):
        # check user variables are valid
        if not is_null_or_whitespace(self.userName.text) and self.validateDate():
            unit_of_work = MolineriaUnitOfWork("data/molineria.db")
            with unit_of_work:
                parsed_date: date | None = None
                if not self.dob or not is_null_or_whitespace(self.dob.text):
                    parsed_date = datetime.strptime(self.dob.text, "%Y-%m-%d").date()

                user = User(
                    name=self.userName.text,
                    date_of_birth=parsed_date,
                    comment=self.comments.text,
                )
                try:
                    inserted_user = unit_of_work.user_repo.create(user)
                    logger.debug(f"INSERTED USER: {inserted_user}")
                    self.reset()
                    return True
                except UniqueConstraintException:
                    PopupUtil.error("Duplicate Name")
                    return False

        else:
            PopupUtil.error("Invalid Name or Date")
            return False

    # reset user variable
    def reset(self):
        self.userName.text = ""
        self.comments.text = ""
        self.dob.text = ""

    # check date
    def validateDate(self):
        if not self.dob or is_null_or_whitespace(self.dob.text):
            return True
        try:
            datetime.strptime(self.dob.text, "%Y-%m-%d")
            return True
        except ValueError:
            return False


