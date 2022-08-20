from kivy.app import App
from data.models import User


class StateStore:
    last_page: str = ""
    current_page: str = ""
    current_user: User
    selected_user_medication_id: int = 0

    @property
    def app_title(self) -> str:
        return get_app().title

    @app_title.setter
    def app_title(self, value: str | None) -> None:
        get_app().title = value


# needed for getting MyApp without circle dep issue
def get_app() -> App:
    instance = App.get_running_app()
    if instance:
        return instance
    raise Exception("Failed to get running app")


def get_state() -> StateStore:
    return get_app().state
