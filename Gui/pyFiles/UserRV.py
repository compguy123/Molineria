from kivy.uix.recycleview import RecycleView

class UserRV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def refreshMeds(self, data):
        self.data = data