"""
Hotkey listener module for SnakePit Clicker.

Handles global key combinations for starting, stopping, and exiting the auto clicker.

:author: sora7672
"""

__author__ = 'sora7672'

from threading import Thread, Lock, Event

from pynput import mouse, keyboard
from time import sleep

from config_loader import ConfigHolder
from click_worker import start_clicker, stop_clicker, is_clicker_alive


class HotkeyListener:
    """
    Singleton class for monitoring keyboard input and triggering clicker actions based on user-defined hotkeys.

    Attributes:
        _lock (Lock): Ensures thread-safe access to internal state
        _stop_event (Event): Signals listener thread to stop
        _thread (Thread): The background listener thread
        _clicker_alive (bool): Indicates whether the clicker is running
        _current_pressed_keys (set[str]): Currently held keys
        _exit_key_combo (set[str]): Key combo to exit application
        _start_key_combo (set[str]): Key combo to start clicker
        _stop_key_combo (set[str]): Key combo to stop clicker
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Creates and returns the singleton instance of HotkeyListener.

        :return: HotkeyListener (The singleton instance)
        """

        if cls._instance is None:
            cls._instance = super(cls, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the hotkey listener, sets up key combinations, and starts the listener thread.

        :return: None (no return value)
        """

        if hasattr(self, '_initialized'):
            return

        self._initialized:bool = True
        self._lock = Lock()
        self._stop_event = Event()
        self._thread = Thread(target=self.__key_listener)
        self._clicker_alive: bool = False

        self._current_pressed_keys: set[str] = set()
        self.__set_settings()

        self._thread.start()

    @property
    def clicker_alive(self) -> bool:
        """
        Gets the internal flag indicating whether the clicker is running.

        :return: bool (Clicker running status)
        """

        with self._lock:
            return self._clicker_alive

    @clicker_alive.setter
    def clicker_alive(self, value: bool) -> None:
        """
        Sets the internal flag indicating the clicker running status.

        :param value: bool (New status of clicker)
        :return: None (no return value)
        """

        with self._lock:
            self._clicker_alive = value

    def __set_settings(self) -> None:
        """
        Fetches hotkey combinations from the configuration and validates them.

        :return: None (no return value)
        """

        with self._lock:
            self._exit_key_combo: set[str] = self.__validate_keys(ConfigHolder().exit_key_combo)
            self._start_key_combo: set[str] = self.__validate_keys(ConfigHolder().start_key_combo)
            self._stop_key_combo: set[str] = self.__validate_keys(ConfigHolder().stop_key_combo)

    def __validate_keys(self, key_tuple) -> set:
        """
        Validates all key values in the given key combo.

        :param key_tuple: tuple (Tuple of key strings)
        :return: set (Validated key set)
        :raises TypeError: If a key is not a string
        :raises ValueError: If a key is not lowercase or invalid
        """

        for key_value in key_tuple:
            if not isinstance(key_value, str):
                raise TypeError(f'From ({key_tuple}) - Key {key_value} is not a string.')

            if len(key_value) == 1 and not key_value.islower():
                raise ValueError(f'From ({key_tuple}) - Key {key_value} is not lower case.')

            if len(key_value) != 1 and not hasattr(keyboard.Key, key_value.lower()):
                raise ValueError(f'From ({key_tuple}) - Key "{key_value}" is not a valid special key.')

        return set(key_tuple)

    def __exit_program(self):
        """
        Triggers the listener to stop and prepares program shutdown.

        :return: None (no return value)
        """

        with self._lock:
            self._stop_event.set()

    def __check_hotkeys(self):
        """
        Triggers the listener to stop and prepares program shutdown.

        :return: None (no return value)
        """

        with self._lock:
            do_exit = all([k in self._current_pressed_keys for k in self._exit_key_combo])
            do_stop = all([k in self._current_pressed_keys for k in self._stop_key_combo])
            do_start = all([k in self._current_pressed_keys for k in self._start_key_combo])

        if do_exit:
            if self.clicker_alive:
                stop_clicker()
                self.clicker_alive = False
            self.__exit_program()
            print("...SnakePit gracefully shut down.")
            return

        if self.clicker_alive:
            if do_stop:
                stop_clicker()
                self.clicker_alive = False
        else:
            if do_start:
                start_clicker()
                self.clicker_alive = True

    def _get_key_value(self, key):
        """
        Converts a pynput key object to a lowercase string representation.

        :param key: Key (pynput keyboard key object)
        :return: str | None (Lowercase string or None)
        """

        if not key or key is None:
            return
        if isinstance(key, keyboard.Key):
            return key.name.lower()
        else:
            if key.char is None:
                return 
            return key.char.lower()

    def _key_push(self, key):
        """
        Handles key press events by adding key to active set and checking hotkeys.

        :param key: Key (Pressed key object)
        :return: None (no return value)
        """

        if not key or key is None:
            return
        key_value = self._get_key_value(key)
        if key_value == "" or key_value is None:
            return
        with self._lock:
            self._current_pressed_keys.add(key_value)
        self.__check_hotkeys()


    def _key_release(self, key):
        """
        Handles key release events by removing the key from active set.

        :param key: Key (Released key object)
        :return: None (no return value)
        """

        if not key:
            return
        key_value = self._get_key_value(key)
        with self._lock:
            self._current_pressed_keys.discard(key_value)

    def __key_listener(self):
        """
        Main keyboard listener loop that monitors for hotkey triggers.

        :return: None (no return value)
        """

        with keyboard.Listener(on_press=self._key_push, on_release=self._key_release) as listener:
            while not self._stop_event.is_set():
                sleep(0.1)
            listener.stop()


if __name__ == '__main__':
    print("Please start with the main.py!")
