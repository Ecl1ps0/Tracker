def save_clipboard_content(clipboard_content: str, path: str = ".\\clipboard.txt") -> None:
    with open(path, 'a') as file:
        file.write(clipboard_content + "\n")


def save_to_report(content: str, path: str) -> None:
    with open(path, "a") as file:
        file.write(content + "\n")
