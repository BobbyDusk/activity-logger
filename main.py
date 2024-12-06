from pathlib import Path
import datetime
import pyscreenshot as ImageGrab
from PIL import Image, ImageDraw, ImageFont
import subprocess
import re


activity_logger_path = Path(Path.home(), "activity_logger")


def get_date_string() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")

    
def get_date_time_string() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


def check_if_date(date_string) -> bool:
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_string))


def create_video_from_images_in_folder(folder_path: Path) -> None:
    fps = 2
    subprocess.run([
        "ffmpeg", 
        "-framerate", f"{fps}", 
        "-pattern_type", "glob",
        "-i", f"{folder_path}/*.jpg", 
        "-vcodec", "libx265", 
        "-y", f"{folder_path}/video.mp4"
    ])
    

def check_if_video_exists(folder_path: Path) -> bool:
    return Path(folder_path, "video.mp4").exists()


def list_directories(folder_path: Path) -> list:
    dirs = [p.name for p in folder_path.iterdir() if p.is_dir() and check_if_date(p.name)]
    return sorted(dirs)


def get_previous_folder_path() -> Path:
    directories = list_directories(activity_logger_path)
    if len(directories) >= 2:
        newest_folder = directories[-2]
        return Path(activity_logger_path, newest_folder)
    else:
        return None

    
def process_previous_folder() -> None:
    folder_path = get_previous_folder_path()
    if folder_path and not check_if_video_exists(folder_path):
        create_video_from_images_in_folder(folder_path)


def write_text_on_image(image: Image, text: str) -> Image:
    draw = ImageDraw.Draw(image)

    # Define the font and size (you can specify a TTF file and size)
    font = ImageFont.truetype("Arial.ttf", 24)  # Load Arial font with size 24

    position = (20, 20)
    text_color = "white"
    draw.text(position, text, font=font, fill=text_color)

    position = (20, 45)
    text_color = "black"
    draw.text(position, text, font=font, fill=text_color)


    return image

        
def write_date_time_on_image(image) -> Image:
    date_time = get_date_time_string()
    return write_text_on_image(image, date_time)


def run():
    log_path = Path(activity_logger_path, "log.txt")
    with open(str(log_path), "a") as f:
        f.write(f"\n{get_date_time_string()} - ")

    try:
        # process_previous_folder()

        dir_path = Path(activity_logger_path, get_date_string())
        dir_path.mkdir(parents=True, exist_ok=True)

        # Capture the entire screen
        screenshot = ImageGrab.grab()

        # convert to rgb
        screenshot = screenshot.convert("RGB")

        # Write the date and time on the image
        screenshot = write_date_time_on_image(screenshot)

        file_path = Path(dir_path, f"{get_date_time_string()}.jpg")
        with open(str(file_path), "w") as f:
            screenshot.save(f, quality=10)
        with open(str(log_path), "a") as f:
            f.write(f"Screenshot saved to {str(file_path)}")
    except Exception as e:
        with open(str(log_path), "a") as f:
            f.write(f"Error: {e}")


if __name__ == "__main__":
    run()