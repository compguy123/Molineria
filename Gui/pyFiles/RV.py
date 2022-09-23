import logging
import os
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button

from Gui.pyFiles.BaseRecyclerViewer import BaseRecyclerViewer
from Gui.pyFiles.navigation_manager import NavigationManager
from Gui.pyFiles.state_store import get_state
from data.models import DayOfWeek, User, UserMedicationDetailWithIntakeDTO
from data.specifications import GetAllUsersOrderedSpec, GetAllUsersMedicationDetailsWithIntakes
from data.unit_of_work import MolineriaUnitOfWork
from datetime import date, timedelta

from util.string import to_date

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger().getChild(__name__)


class RV(BaseRecyclerViewer):
    @property
    def rv_data(self):
        return self.data

    def refresh_data(self):
        logger.info(f"<{__class__.__name__}> refreshing list")
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            spec = GetAllUsersOrderedSpec(unit_of_work)
            users = spec.execute()
            if users:
                self.data = [{"text": u.name, "id": u.id, "user": self} for u in users]

    def getApp(self, id: int):
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            state = get_state()
            user = unit_of_work.user_repo.get(id)
            if not user:
                raise Exception(f"failed to get user {id}")
            state.current_user = user
            NavigationManager.go_left("UserPage")


class SelectableLabel(Button):
    user: RV = ObjectProperty(None)
    id: int

    def calculate_last_login_date(self, user: User, unit_of_work):
        spec = GetAllUsersMedicationDetailsWithIntakes(unit_of_work, user.id)
        user_meds = spec.execute()
        start = to_date(user.last_login_date)
        end = date.today()
        print(start, end)

        meds_to_discard: list[UserMedicationDetailWithIntakeDTO] = []
        while start != end:
            print(start)
            day_of_week = DayOfWeek.fromdate(start)

            for user_med, intakes in user_meds:
                for intake in intakes:
                    check_intake_done = False
                    if intake.has_day_of_week(day_of_week):
                        um = user_med.user_medication
                        um.total_weight_in_milligrams = um.total_weight_in_milligrams - intake.amount_in_milligrams
                        um.quantity = um.total_weight_in_milligrams / um.weight_in_milligrams
                        unit_of_work.user_medication_repo.update(um)
                        check_intake_done = um.total_weight_in_milligrams < 0
                        if check_intake_done:
                            meds_to_discard.append(user_med)
                            break

            start = start + timedelta(days=1)

        for med in meds_to_discard:
            unit_of_work.user_medication_repo.delete(med.user_medication.id)

        def med_name(med: UserMedicationDetailWithIntakeDTO):
            return f"<li>{med.medication.name}</li>"

        if any(meds_to_discard):
            med_names = "\n\t".join(map(med_name, meds_to_discard))
            message = Mail(
                from_email='larencastelino@yahoo.ca',
                to_emails=user.email,
                subject="Molineria Alert",
                html_content=f"""
                The following medications need a refill:
                <ul>
                {med_names}
                </ul>
                """)
            print(message.content)
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)

    def on_release(self, **kwargs):
        super().on_release()
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            user = unit_of_work.user_repo.get(self.id)
            if user.last_login_date:
                self.calculate_last_login_date(user, unit_of_work)
            user.last_login_date = date.today()
            unit_of_work.user_repo.update(user)
        self.user.getApp(self.id)
