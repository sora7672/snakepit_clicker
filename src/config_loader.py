"""
Configuration manager module for SnakePit Clicker.

Provides a singleton class for managing user settings like key bindings
and click intervals from a persistent JSON file.

:author: sora7672
"""

__author__ = 'sora7672'

from threading import Lock, Event
import json
from warnings import warn
from os import path, rename, makedirs
from datetime import datetime
from pynput import keyboard


class ConfigHolder:
    """
    Singleton class for loading, validating, and persisting configuration settings.

    Attributes:
        _lock (Lock): Ensures thread-safe access to configuration values
        _file_name (str): Name of the JSON file containing settings
        _path (str): Optional custom path for config storage
        _project_path (str): Root path of the project (used if _path is not set)
        _file_path (str): Full resolved path to the JSON config file
        _start_key_combo (tuple): Keys to start the clicker
        _stop_key_combo (tuple): Keys to stop the clicker
        _exit_key_combo (tuple): Keys to exit the program
        _interval_clicks (int): Time between clicks in milliseconds
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Creates and returns the singleton instance of ConfigHolder.

        :return: ConfigHolder (The singleton instance)
        """

        if cls._instance is None:
            cls._instance = super(cls, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the configuration, sets default values, and loads from file if available.

        :return: None (no return value)
        """

        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self._lock = Lock()

        self._file_name: str = "config.json"
        self._path: str = ""
        self._project_path = path.abspath(path.join(path.dirname(__file__), '..'))
        if self._path:
            self._path = path.abspath(self._path)
            if not path.exists(self._path):
                makedirs(self._path, exist_ok=True)
            self._file_path: str = path.join(self._path, self._file_name)
        else:
            self._file_path: str = path.join(self._project_path, self._file_name)

        # set default keys
        self._start_key_combo: tuple = ("shift", "s")
        self._stop_key_combo: tuple = ("shift", "s")
        self._exit_key_combo: tuple = ("shift", "e")

        self._interval_clicks: int = 100  # 10x per second

        self.__read_in_settings()

    def __read_in_settings(self) -> None:
        """
        Reads the configuration from the JSON file and applies it to internal attributes.

        Handles defaulting and error recovery for missing or invalid data.

        :return: None (no return value)
        """

        if not path.exists(self._file_path):
            warn(f"The file {self._file_path} does not exist. Using default settings.")
            self.__save_settings()
            return

        with open(self._file_path, 'r') as file:
            content = file.read().strip()
        if content == "":
            warn(f"The file {self._file_path} is empty. Using default settings.")
            self.__save_settings()
            return

        try:
            tmp_config = json.loads(content)
        except json.JSONDecodeError:
            warn(f"The file {self._file_path} contains invalid JSON. Using default settings.")
            self.__save_broken_json()
            self.__save_settings()
            return

        if not tmp_config:
            warn(f"The file {self._file_path} is empty. Using default settings.")
            self.__save_settings()
            return

        if not all(["_start_key_combo" in tmp_config, "_stop_key_combo" in tmp_config,
                   "_exit_key_combo" in tmp_config,"_interval_clicks" in tmp_config]):
            warn(f"""
            The file {self._file_path} has not all needed keys. 
            Needed keys:
            '_start_key_combo', '_stop_key_combo', '_exit_key_combo', '_interval_clicks'
            Using default settings.
            """)
            self.__save_settings()
            return

        if not isinstance(tmp_config["_interval_clicks"], int):
            raise TypeError("The interval clicks needs to be an integer.")
        if tmp_config["_interval_clicks"] <= 5:
            raise ValueError("The interval clicks needs to be a integer higher than 5.")


        with self._lock:
            self._start_key_combo = self.__validate_keys(tmp_config["_start_key_combo"])
            self._stop_key_combo = self.__validate_keys(tmp_config["_stop_key_combo"])
            self._exit_key_combo = self.__validate_keys(tmp_config["_exit_key_combo"])


            self._interval_clicks = tmp_config["_interval_clicks"]

    def __validate_keys(self, key_tuple) -> set:
        """
        Validates that all entries in the key tuple are proper key strings.

        :param key_tuple: tuple (Tuple of key names to validate)
        :return: set (Set of validated key names)
        :raises TypeError: If a key is not a string
        :raises ValueError: If a key is not lowercase or invalid as a special key
        """
        # TODO: Outsource duplication
        for key_value in key_tuple:
            if not isinstance(key_value, str):
                raise TypeError(f'From ({key_tuple}) - Key {key_value} is not a string.')

            if len(key_value) == 1 and not key_value.islower():
                raise ValueError(f'From ({key_tuple}) - Key {key_value} is not lower case.')

            if len(key_value) != 1 and not hasattr(keyboard.Key, key_value.lower()):
                raise ValueError(f'From ({key_tuple}) - Key "{key_value}" is not a valid special key.')

        return set(key_tuple)

    def __save_settings(self) -> None:
        """
        Saves the current configuration to the JSON file.

        :return: None (no return value)
        """

        tmp_config = dict()

        with self._lock:
            tmp_config["_start_key_combo"] = self._start_key_combo
            tmp_config["_stop_key_combo"] = self._stop_key_combo
            tmp_config["_exit_key_combo"] = self._exit_key_combo
            tmp_config["_interval_clicks"] = self._interval_clicks

        with open(self._file_path, 'w') as file:
            file.write(json.dumps(tmp_config, indent=4))

    def __save_broken_json(self) -> None:
        """
        Backs up the existing invalid JSON config file with a timestamp suffix.

        :return: None (no return value)
        """

        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime('%Y%m%d-%H%M%S')
        rename(self._file_path, f"{current_datetime}_broken_{self._file_name}")

    @property
    def start_key_combo(self) -> tuple:
        """
        Gets the configured key combination for starting the clicker.

        :return: tuple (Start key combination)
        """

        with self._lock:
            return self._start_key_combo

    @property
    def stop_key_combo(self) -> tuple:
        """
        Gets the configured key combination for stopping the clicker.

        :return: tuple (Stop key combination)
        """

        with self._lock:
            return self._stop_key_combo

    @property
    def exit_key_combo(self) -> tuple:
        """
        Gets the configured key combination for exiting the application.

        :return: tuple (Exit key combination)
        """
        with self._lock:
            return self._exit_key_combo

    @property
    def interval_clicks(self) -> int:
        """
        Gets the configured click interval in milliseconds.

        :return: int (Click interval in ms)
        """

        with self._lock:
            return self._interval_clicks


if __name__ == '__main__':
    print("Please start with the main.py!")
