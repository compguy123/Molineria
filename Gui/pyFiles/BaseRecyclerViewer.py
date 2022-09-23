from abc import ABC, abstractmethod, abstractproperty
from kivy.uix.recycleview import RecycleView


class BaseRecyclerViewer(RecycleView):
    @abstractmethod
    def refresh_data(self):
        pass

    @abstractproperty
    def rv_data(self):
        pass