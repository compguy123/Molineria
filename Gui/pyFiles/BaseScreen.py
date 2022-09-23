from abc import ABC, abstractmethod, abstractproperty

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from Gui.pyFiles.BaseRecyclerViewer import BaseRecyclerViewer


class BaseScreen(Screen):

    def invoke_refresh(self):
        for name in self.widget_rv_names:
            widget = self.ids[name]
            if widget and hasattr(widget, "refresh_data") and callable(widget.refresh_data):
                widget.refresh_data()

    def on_pre_enter(self, *args):
        self.refresh_events = []
        self.widget_rv_names = []
        for widget_name in self.ids:
            widget = self.ids[widget_name]
            if isinstance(widget, BaseRecyclerViewer):
                self.widget_rv_names.append(widget_name)
                event = Clock.schedule_interval(
                    lambda _: self.invoke_refresh(), 0.5
                )
                self.refresh_events.append(event)


    def on_pre_leave(self, *args):
        for name in self.widget_rv_names:
            widget = self.ids[name]
            if widget and hasattr(widget, "data"):
                widget.data =[]
        for event in self.refresh_events:
            if event and callable(event.cancel):
                event.cancel()
