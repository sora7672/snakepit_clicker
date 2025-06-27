"""
Main module of the SnakePit Clicker tool.

Starts the main application by loading the configuration and launching the hotkey listener.

:author: sora7672
"""

__author__ = 'sora7672'


# Later adding movements to mouse cursor
# also adding key clicks per x seconds

from config_loader import ConfigHolder
from hotkey_listener import HotkeyListener


def start_snakepit() -> None:
    """
    Initializes and starts the SnakePit clicker application.

    Loads configuration, displays click interval and key bindings,
    and starts the hotkey listener.

    :return: None (no return value)
    """

    print("Starting SnakePit...\n")
    cfg = ConfigHolder()
    print(f"Click interval(ms): {cfg.interval_clicks} + 5ms between push+release ({cfg.interval_clicks + 5}ms)")
    print(f"Key Bindings:\n"
            f"Start Auto Clicker [{' + '.join([k.upper() for k in cfg.start_key_combo])}]\n"
            f"Stop Auto Clicker [{' + '.join([k.upper() for k in cfg.stop_key_combo])}]\n"
            f"Exit SnakePit [{' + '.join([k.upper() for k in cfg.exit_key_combo])}]")
    HotkeyListener()


if __name__ == '__main__':
    start_snakepit()