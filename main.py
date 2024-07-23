#!/venv/bin/python

from PIL import ImageGrab
from pathlib import Path
import datetime
import time

def main_loop():
    while True:
        # sleep for 5 seconds
        time.sleep(60)

        # get today's date as string
        today = datetime.datetime.now().strftime("%Y%m%d")

        dir_path = Path("log", today)
        dir_path.mkdir(parents=True, exist_ok=True)

        # Capture the entire screen
        screenshot = ImageGrab.grab()

        current_time = datetime.datetime.now().strftime("%H%M%S")
        file_path = Path(dir_path, f"{current_time}.jpg")
        screenshot.save(str(file_path), quality=15)
        print(f"Screenshot saved to {str(file_path)}")

        # Close the screenshot
        screenshot.close()

if __name__ == "__main__":
    main_loop()