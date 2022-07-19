from datetime import datetime
from data.models import Medication, User, UserMedication
from data.unit_of_work import MolineriaUnitOfWork

db = MolineriaUnitOfWork("data/molineria.db")
with db:  # auto close connection
    user = User(name="John Doe", date_of_birth="1998-08-28", comment="some user")
    if not any(lambda u: u.name == user.name, db.user_repo.get_all()):
        user = db.user_repo.create(
            user
        )  # each create and update call is auto wrapped in transaction

    users = db.user_repo.get_all()  # warning, this gets all records in user table
    print("ALL USERS:", users)
    print("John doe USER:", db.user_repo.get(user.id))

    user.comment = f"new comment in town ({datetime.now()})"
    user = db.user_repo.update(user)
    print(user)

    med = Medication(name="SomeMed101")
    if not any(
        filter(lambda m: m.name == med.name, db.medication_repo.get_all())
    ):  # see if med SomeMed101 doesn't exist in medication table
        med = db.medication_repo.create(med)

    um_list = db.user_medication_repo.get_all()
    if not any(lambda um: um.rx_number == "18282-191S", um_list):
        um = UserMedication(
            user_id=user.id, medication_id=med.id, rx_number="18282-191S", quantity=20
        )
        um = db.user_medication_repo.create(um)
        print(um)
