from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime


class Homepage(Screen):
    pass


class InsertUser(Screen):
    userName = ObjectProperty(None)
    comments = ObjectProperty(None)
    dob = ObjectProperty(None)

    def createUser(self):
        # check user variables are valid
        if self.userName.text != "" and self.validateDate():

            self.reset()
            windowManager.current = "ShowUser"
        else:
            invalidUser()

    # reset user variable
    def reset(self):
        self.userName.text = ""
        self.comments.text = ""
        self.dob.text = ""

    def homepage(self):
        # return to homepage
        windowManager.current = "Homepage"

    # check date
    def validateDate(self):
        try:
            datetime.strptime(self.dob.text, '%Y-%m-%d')
            return True
        except ValueError as ex:
            return False


class ShowUser(Screen):
    pass


class WindowManager(ScreenManager):
    pass


# load kv file
kv = Builder.load_file("my.kv")

# screen manager
windowManager = WindowManager()

# change screens in code
screens = {Homepage(name="Homepage"), InsertUser(name="InsertUser"), ShowUser(name="ShowUser")}
for screen in screens:
    windowManager.add_widget(screen)


# create pipup
def invalidUser():
    pop = Popup(title='Error',
                content=Label(text='Invalid name or date.'),
                size_hint=(.4, .4))
    pop.open()


class MyApp(App):
    def build(self):
        return windowManager


if __name__ == "__main__":
    MyApp().run()
