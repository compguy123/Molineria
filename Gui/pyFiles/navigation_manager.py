import logging
from Gui.pyFiles.state_store import get_app, get_state

logger = logging.getLogger().getChild(__name__)


class NavigationManager:
    @staticmethod
    def go(page: str, dir: str | None = None) -> None:
        app = get_app()
        if app and app.root:
            screen_manager = app.root

            state = get_state()
            state.last_page = screen_manager.current  # type: ignore
            state.current_page = page  # type: ignore

            if dir is not None:
                screen_manager.transition.direction = dir  # type: ignore

            screen_manager.current = page  # type: ignore

            logger.info(f"<{__class__.__name__}> {state.last_page} -> {page}")

    @staticmethod
    def go_right(page: str) -> None:
        NavigationManager.go(page, "right")

    @staticmethod
    def go_left(page: str) -> None:
        NavigationManager.go(page, "left")
