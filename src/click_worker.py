"""
Click worker module for SnakePit Clicker.

Provides the AutoClicker class as a singleton responsible for simulating mouse clicks
in a separate thread based on a configured interval.

:author: sora7672
"""

__author__ = 'sora7672'

from pynput import mouse, keyboard
from pynput.mouse import Button as MouseButton
from threading import Thread, Lock, Event
from time import sleep

from config_loader import ConfigHolder

# Just some test for key sends for later
# def push_key(key_name: str):
#     if not key_name or not isinstance(key_name, str):
#         return
#     if len(key_name) >= 2 and key_name not in pynput.keyboard.Key:
#         print("no key for inputs")
#         return
#
#     keyboard_controller = keyboard.Controller()
#     keyboard_controller.press(key_name)
#     wait_ms(5)
#     keyboard_controller.release(key_name)


def wait_ms(ms:int) -> None:
    """
    Waits for a specified duration in milliseconds.

    :param ms: int (Duration to wait in milliseconds)
    :return: None (no return value)
    """

    sleep(ms/1000)


class AutoClicker:
    """
    Singleton class that manages automated mouse clicking in a background thread.

    Attributes:
        _initialized (bool): Ensures initialization runs only once
        _lock (Lock): Thread lock for potential synchronization (unused currently)
        _stop_event (Event): Signal to start or stop the click worker
        _thread (Thread): The worker thread executing clicks
        _mouse_controller (Controller): Controls mouse actions
        _keyboard_controller (Controller): Controls keyboard actions (unused)
        _mouse_click_interval (int): Interval between clicks in milliseconds
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Implements the singleton pattern by ensuring only one instance of the class exists.

        :return: AutoClicker (The singleton instance.)
        """

        if cls._instance is None:
            cls._instance = super(cls, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the singleton AutoClicker with required components and default state.

        :return: None (no return value)
        """

        if hasattr(self, '_initialized'):
            return

        self._initialized: bool = True
        self._lock = Lock()
        self._stop_event = Event()
        self._stop_event.set()

        self._thread = Thread(target=self._click_worker, daemon=True)
        self._mouse_controller = mouse.Controller()
        self._keyboard_controller = keyboard.Controller()

        self._mouse_click_interval = ConfigHolder().interval_clicks


    def _click_worker(self) -> None:
        """
        Internal worker method executed by the background thread.

        Performs left mouse clicks in a loop with the configured interval,
        until the stop event is triggered.

        :return: None (no return value)
        """

        while not self._stop_event.is_set():
            wait_ms(self._mouse_click_interval)
            self._mouse_controller.press(MouseButton.left)
            wait_ms(5)
            self._mouse_controller.release(MouseButton.left)

    def start_clicker(self) -> None:
        """
        Starts the clicker if it is currently stopped by launching the worker thread.

        :return: None (no return value)
        """

        if self._stop_event.is_set():
            self._stop_event.clear()
            self._thread = Thread(target=self._click_worker, daemon=True)
            self._thread.start()

    def stop_clicker(self) -> None:
        """
        Stops the clicker if it is currently running by signaling the stop event
        and joining the worker thread.

        :return: None (no return value)
        """

        if not self._stop_event.is_set():
            self._stop_event.set()
            if self._thread.is_alive():
                self._thread.join()

    def is_clicker_alive(self) -> bool:
        """
        Checks if the click worker is currently running.
        NYI

        :raises NotImplementedError: Function is not yet implemented
        :return: bool (Indicates whether the clicker is alive – currently unreachable)
        """

        raise NotImplementedError("clicker alive is faulty, needs better handling!")
        return self._stop_event.is_set()

def stop_clicker() -> None:
    """
    Stops the singleton AutoClicker instance.

    :return: None (no return value)
    """

    AutoClicker().stop_clicker()

def start_clicker() -> None:
    """
    Starts the singleton AutoClicker instance.

    :return: None (no return value)
    """

    AutoClicker().start_clicker()

def is_clicker_alive() -> bool:
    """
    Checks if the singleton AutoClicker instance is alive.
    NYI

    :raises NotImplementedError: Function is not yet implemented
    :return: None (no return value – always, due to unimplemented method)
    """
    raise NotImplementedError()
    AutoClicker().is_clicker_alive()


if __name__ == '__main__':
    print("Please start with the main.py!")
