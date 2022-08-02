from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from data.specifications import GetAllUsersOrderedSpec
from data.unit_of_work import MolineriaUnitOfWork


class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def refreshList(self):
        # assigning data in RecyclerView
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            spec = GetAllUsersOrderedSpec(unit_of_work.user_repo)
            users = spec.execute()
            if users:
                self.data = [
                    {"text": u.name, "id": u.id, "user": self} for u in users
                ]

    def getApp(self, id):
        # get id
        app = App.get_running_app()
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            app.user_name = unit_of_work.user_repo.get(id).name
            app.user_DOB= unit_of_work.user_repo.get(id).date_of_birth
        app.root.current = "UserPage"
        app.root.transition.direction = "left"


class SelectableLabel(Button):
    # get User
    user = ObjectProperty()

    def on_release(self, **kwargs):
        super().on_release()
        self.user.getApp(self.id)
