from kivy.app import App
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from data.unit_of_work import MolineriaUnitOfWork


class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def refreshList(self):
        # assigning data in RecyclerView
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            users = unit_of_work.user_repo.get_all()
            if users:
                self.data = [{'text': str(u.name), "UserId": u.id} for u in users]


class SelectableLabel(Button):
    def on_release(self, **kwargs):
        super().on_release()
        print(self.UserId)
