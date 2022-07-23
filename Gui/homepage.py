from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class Homepage(Screen):
    pass


class InsertUser(Screen):
    firstName = ObjectProperty(None)
    lastName = ObjectProperty(None)

    def createUser(self):
        if self.firstName.text != "" and self.lastName.text != "":
            # get add user in database
            
            self.reset()
            windowManager.current = "ShowUser"
        else:
            invalidUser()

    def reset(self):
        self.firstName.text = ""
        self.lastName.text = ""

    def homepage(self):
        # return to homepage
        windowManager.current = "Homepage"


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
    pop = Popup(title='Invalid User',
                content=Label(text='Invalid first or last name.'),
                size_hint=(.4, .4))
    pop.open()


class MyApp(App):
    def build(self):
        return windowManager


if __name__ == "__main__":
    MyApp().run()
