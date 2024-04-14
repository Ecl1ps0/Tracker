import keyboard

from configs.file_writers import save_to_report

double_hotkeys = [
    ("ctrl+c", "Copy"),
    ("ctrl+v", "Paste"),
    ("ctrl+x", "Cut"),
    ("ctrl+d", "Tab"),
    ("ctrl+a", "Highlight All"),
    ("ctrl+e", "Search Panel"),
    ("ctrl+l", "Search Panel"),
    ("ctrl+z", "Undo"),
    ("ctrl+f", "Find"),
    ("ctrl+n", "Open New Browser Window"),
    ("ctrl+o", "Open Tab with Local File"),
    ("ctrl+p", "Print"),
    ("ctrl+r", "Update Page"),
    ("ctrl+w", "Close Tab"),
    ("ctrl+h", "Open History"),
    ("ctrl+t", "Open New Tab"),
    ("ctrl+right", "Go Back"),
    ("ctrl+left", "Go Next"),
    ("ctrl+up", "Go to the Beginning"),
    ("ctrl+down", "Go to the End"),
    ("ctrl+esc", "Open Windows Bar"),
    ("ctrl+tab", "Change tab"),
    ("alt+tab", "Change window"),
    ("cmd+d", "Close all windows"),
    ("cmd+tab", "Choose workspace"),
]


def register_hotkeys() -> None:
    for shortcut, name in double_hotkeys:
        keyboard.add_hotkey(shortcut, save_to_report, args=(name, ".\\report.txt"))
