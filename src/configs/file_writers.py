import os
from datetime import datetime


def save_clipboard_content(clipboard_content: str, path: str = ".\\temp\\clipboard.txt") -> None:
    with open(path, 'a') as file:
        file.write(clipboard_content + "\n")


def save_to_report_with_time(content: str, path: str = ".\\temp\\report.txt") -> None:
    with open(path, "a") as file:
        file.write(content + " " + datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3] + "\n")


def save_to_report(content: str, path: str = ".\\temp\\report.txt") -> None:
    with open(path, "a") as file:
        file.write(content + "\n")


def clear_temp(directory: str = ".\\temp") -> None:
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                open(file_path, 'w').close()  # Remove the file
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
