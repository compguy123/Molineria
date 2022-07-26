from kivy.uix.recycleview import RecycleView

from data.unit_of_work import MolineriaUnitOfWork


class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # assigning data in RecyclerView
        unit_of_work = MolineriaUnitOfWork("data/molineria.db")
        with unit_of_work:
            users = unit_of_work.user_repo.get_all()
            self.data = [{'text': str(u.name)} for u in users]
