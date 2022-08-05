import logging
from kivy.uix.recycleview import RecycleView

logger = logging.getLogger().getChild(__name__)

class UserRV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def refreshMeds(self, data):
        self.data = data