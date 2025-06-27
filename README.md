# Snakepit Clicker

**Snakepit Clicker** is a minimal global auto-clicker with configurable hotkeys and click intervals. All settings are managed through a JSON file.

---
## Features

- Automatic mouse clicking at a custom interval
- Global hotkeys for start, stop, and exit
- Configuration stored in `config.json`
- Singleton-based design for clicker and listener
- Lightweight and headless

---
## Installation

1. Make sure you have `pynput` installed:

   ```bash
   pip install pynput
   ```

2. Run the main script:

   ```bash
   python main.py
   ```

A `config.json` file will be created automatically if it doesn’t exist.

---
## Configuration (`config.json`)

```json
{
    "_start_key_combo": ["shift", "s"],
    "_stop_key_combo": ["shift", "s"],
    "_exit_key_combo": ["shift", "e"],
    "_interval_clicks": 100
}
```

- **_start_key_combo**: Key combination to start the clicker
- **_stop_key_combo**: Key combination to stop it
- **_exit_key_combo**: Key combination to exit the program
- **_interval_clicks**: Interval between clicks in milliseconds (must be > 5)

---
## Project Structure

- `main.py` – Entry point
- `click_worker.py` – Background click engine
- `hotkey_listener.py` – Listens for global key events
- `config_loader.py` – Loads and validates configuration

---
## Notes

- The hotkeys work globally as long as the script is running.
- Default keys use lowercase letters or special names (`shift`, `ctrl`, etc.).
- The clicker adds 5ms between press and release for each click.

---
## Future Updates
As of today (27.06.25) this is just a small POC.
I will expand this when I've more time again with:
- macro functions  
- import/export macros
- record mouse & keyboard inputs to repeat  
 
*and much later:*
- fake usb interface to emulate mouse & keyboard as a listener for this tool
- maybe reading in screens for advanced usage