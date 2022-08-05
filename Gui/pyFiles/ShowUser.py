import logging
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock, ClockEvent
from Gui.pyFiles.RV import RV

logger = logging.getLogger().getChild(__name__)


class ShowUser(Screen):
    def on_pre_enter(self, *args):
        user_list: RV = self.ids.userList
        user_list.refreshList()
        self.refresh_list_event: ClockEvent = Clock.schedule_interval(
            lambda _: user_list.refreshList(), 0.5
        )

    def on_pre_leave(self):
        if self.refresh_list_event and callable(self.refresh_list_event.cancel):
            self.refresh_list_event.cancel()
