#!/venv/bin/python

from PIL import ImageGrab
from pathlib import Path
import datetime

def run():
    activity_logger_path = Path(Path.home(), "activity_logger")
    log_path = Path(activity_logger_path, "log.txt")
    datetime_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(str(log_path), "a") as f:
        f.write(f"\n{datetime_string} - ")

    try:
        # get today's date as string
        today = datetime.datetime.now().strftime("%Y%m%d")

        dir_path = Path(activity_logger_path, today)
        dir_path.mkdir(parents=True, exist_ok=True)

        # Capture the entire screen
        screenshot = ImageGrab.grab()

        current_time = datetime.datetime.now().strftime("%H%M%S")
        file_path = Path(dir_path, f"{current_time}.jpg")
        with open(str(file_path), "w") as f:
            screenshot.save(f, quality=15)
        with open(str(log_path), "a") as f:
            f.write(f"Screenshot saved to {str(file_path)}")
    except Exception as e:
        with open(str(log_path), "a") as f:
            f.write(f"Error: {e}")


run()