import logging
from kivy.properties import ObjectProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from Gui.pyFiles.navigation_manager import NavigationManager
from Gui.pyFiles.state_store import get_state
from data.specifications import GetAllUsersOrderedSpec
from data.unit_of_work import MolineriaUnitOfWork

logger = logging.getLogger().getChild(__name__)


class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def refreshList(self):
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

    def on_release(self, **kwargs):
        super().on_release()
        self.user.getApp(self.id)
