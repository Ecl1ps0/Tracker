import keyboard

from datetime import datetime

from configs.file_writers import save_to_report
from configs.logger import get_logger

logger = get_logger(__name__)


class HotkeyManager:
    def __init__(self):
        self.hotkeys = [
            "ctrl+c", "ctrl+v", "ctrl+x", "ctrl+d", "ctrl+a", "ctrl+e",
            "ctrl+l", "ctrl+z", "ctrl+f", "ctrl+n", "ctrl+o", "ctrl+p",
            "ctrl+r", "ctrl+w", "ctrl+h", "ctrl+t", "ctrl+right", "ctrl+left",
            "ctrl+up", "ctrl+down", "ctrl+esc", "ctrl+tab", "alt+tab",
            "cmd+d", "cmd+tab", "cmd+v"
        ]
        self.hotkey_counts = {key: 0 for key in self.hotkeys}

    def increase_hotkey_count(self, shortcut: str) -> None:
        self.hotkey_counts[shortcut] += 1
        logger.info(shortcut + datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3] + "\n")

    def register_hotkeys(self) -> None:
        for shortcut in self.hotkeys:
            keyboard.add_hotkey(shortcut, self.increase_hotkey_count, args=(shortcut,))

    def save_hotkey_counts(self) -> None:
        for key, count in self.hotkey_counts.items():
            logger.info(f"Hotkey: {key} - {count}")
            save_to_report(f"Hotkey: {key} - {count}")
