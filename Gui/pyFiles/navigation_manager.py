from Gui.pyFiles.state_store import get_app


class NavigationManager:
    @staticmethod
    def go(page: str, dir: str) -> None:
        app = get_app()
        if app and app.root:
            screen_manager = app.root
            screen_manager.transition.direction = dir  # type: ignore
            screen_manager.current = page  # type: ignore

    @staticmethod
    def go_right(page: str) -> None:
        app = get_app()
        if app and app.root:
            screen_manager = app.root
            screen_manager.transition.direction = "right"  # type: ignore
            screen_manager.current = page  # type: ignore

    @staticmethod
    def go_left(page: str) -> None:
        app = get_app()
        if app and app.root:
            screen_manager = app.root
            screen_manager.transition.direction = "left"  # type: ignore
            screen_manager.current = page  # type: ignore
