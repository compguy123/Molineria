from data.models import User
from data.unit_of_work import MolineriaUnitOfWork

db = MolineriaUnitOfWork("data/molineria.db")
with db:
    user = User(name="John Doe", date_of_birth="1998-08-28", comment="First user")
    print(f"CREATING: {user.id}, {user.name}, {user.date_of_birth}, {user.comment}")
    user = db.user_repo.create(user)
    print(f"CREATED: {user.id}, {user.name}, {user.date_of_birth}, {user.comment}")
