from datetime import datetime
from data.models import Medication, User, UserMedication
from data.unit_of_work import MolineriaUnitOfWork


def user_name_match(name: str):
    def match_user(m: User) -> bool:
        return m.name == name

    return match_user


def med_name_match(name: str):
    def match_med(m: Medication) -> bool:
        return m.name == name

    return match_med


def user_med_rx_match(rx: str):
    def match_user_med(m: UserMedication) -> bool:
        return m.rx_number == rx

    return match_user_med


db = MolineriaUnitOfWork("molineria/data/molineria.db")
with db:  # auto close connection
    user = User(
        name="John Doe",
        date_of_birth=datetime.strptime("1998-08-28", "%Y-%m-%d").date(),
        comment="some user",
    )
    if not any(filter(user_name_match(user.name), db.user_repo.get_all())):
        user = db.user_repo.create(
            user
        )  # each create and update call is auto wrapped in transaction
        if user is None:
            raise Exception()

    users = db.user_repo.get_all()  # warning, this gets all records in user table
    print("ALL USERS:", users)
    print("John doe USER:", db.user_repo.get(user.id))

    user.comment = f"new comment in town ({datetime.now()})"
    user = db.user_repo.update(user)
    if user is None:
        raise Exception()
    print(user)

    med = Medication(name="SomeMed101")

    if not any(
        filter(med_name_match(med.name), db.medication_repo.get_all())
    ):  # see if med SomeMed101 doesn't exist in medication table
        med = db.medication_repo.create(med)
        if med is None:
            raise Exception()

    um_list = db.user_medication_repo.get_all()
    if not any(filter(user_med_rx_match("18282-191S"), um_list)):
        um = UserMedication(
            user_id=user.id, medication_id=med.id, rx_number="18282-191S", quantity=20
        )
        um = db.user_medication_repo.create(um)
        print(um)
