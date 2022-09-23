import logging
import sys
from kivy.logger import (
    formatter_message,
    ColoredFormatter,
    ConsoleHandler,
)
from Gui.pyFiles.MyApp import MyApp

if __name__ == "__main__":
    logger = logging.root
    color_fmt = formatter_message(
        "(%(asctime)s) [%(levelname)-18s] %(message)s",
        True,
    )
    formatter = ColoredFormatter(color_fmt, use_color=True)
    formatter.datefmt = "%Y-%m-%d %H:%M:%S"
    console = ConsoleHandler(sys.stdout)
    console.setFormatter(formatter)

    for h in logger.handlers:
        if isinstance(h, ConsoleHandler):
            logger.removeHandler(h)
    logger.addHandler(console)

    MyApp().run()
