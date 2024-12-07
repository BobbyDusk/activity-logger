from pathlib import Path
import datetime
import pyscreenshot as ImageGrab
from PIL import Image, ImageDraw, ImageFont
import subprocess
import re


activity_logger_path = Path(Path.home(), "activity_logger")
font_path = Path(activity_logger_path, ".src/Arial.ttf")


def get_time_string_from_date(date: datetime.datetime) -> str:
    return date.strftime("%H:%M:%S")


def get_date_string() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")

    
def get_day_of_week_string() -> str:
    return datetime.datetime.now().strftime("%A")

    
def get_date_time_string_from_date(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%d_%H:%M:%S")

    
def get_date_time_string() -> str:
    return get_date_time_string_from_date(datetime.datetime.now())


def check_if_date(date_string) -> bool:
    pattern = r'^\d{4}-\d{2}-\d{2}'
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

    
def create_text_image(text: str) -> Image:
    image = Image.new("RGB", (1920, 1080), color="black")
    draw = ImageDraw.Draw(image)
    font_size = 48
    font = ImageFont.truetype(font_path, font_size)
    text_width = draw.textlength(text, font=font)
    text_height = font_size
    position = (image.width // 2 - text_width // 2, image.height // 2 - text_height // 2)
    text_color = "white"
    draw.text(position, text, font=font, fill=text_color)
    return image


def process_start_time(time: datetime.datetime, folder_path: Path) -> None:
    start_time = time - datetime.timedelta(minutes=1)
    text = f"START {get_time_string_from_date(start_time)}"
    image = create_text_image(text)
    for i in range(5):
        image_path = Path(folder_path, f"{get_date_time_string_from_date(start_time)}_START_{i}.jpg")
        image.save(image_path)


def process_stop_time(time: datetime.datetime, folder_path: Path) -> None:
    stop_time = time + datetime.timedelta(minutes=1)
    text = f"STOP {get_time_string_from_date(stop_time)}"
    image = create_text_image(text)
    for i in range(5):
        image_path = Path(folder_path, f"{get_date_time_string_from_date(stop_time)}_STOP_{i}.jpg")
        image.save(image_path)

        
def insert_start_stop_images(folder_path: Path) -> None:
    files = sorted(list(folder_path.glob("*.jpg")))
    previous_date_time = None
    for index, image_path in enumerate(files):
        date_time = datetime.datetime.strptime(image_path.stem, "%Y-%m-%d_%H:%M:%S")
        if index == 0:
            process_start_time(date_time, folder_path)
        elif index == len(files) - 1:
            process_stop_time(date_time, folder_path)
        elif date_time - previous_date_time >= datetime.timedelta(minutes=5):
            process_stop_time(previous_date_time, folder_path)
            process_start_time(date_time, folder_path)
        previous_date_time = date_time

        
def move_video_and_remove_folder(folder_path: Path) -> None:
    video_path = Path(folder_path, "video.mp4")
    new_video_path = Path(activity_logger_path, f"{folder_path.name}.mp4")
    video_path.rename(new_video_path)
    # subprocess.run(["rm", "-rf", folder_path])

    
def process_previous_folder() -> None:
    folder_path = get_previous_folder_path()
    if folder_path:
        insert_start_stop_images(folder_path)
        create_video_from_images_in_folder(folder_path)
        move_video_and_remove_folder(folder_path)

        
def write_date_time_on_image(image) -> Image:
    date_time = get_date_time_string()

    draw = ImageDraw.Draw(image)

    # Define the font and size (you can specify a TTF file and size)
    font = ImageFont.truetype(font_path, 24)  # Load Arial font with size 24

    position = (20, 20)
    text_color = "white"
    draw.text(position, date_time, font=font, fill=text_color)

    position = (20, 45)
    text_color = "black"
    draw.text(position, date_time, font=font, fill=text_color)

    return image


def run():
    log_path = Path(activity_logger_path, "log.txt")
    with open(str(log_path), "a") as f:
        f.write(f"\n{get_date_time_string()} - ")

    try:
        dir_path = Path(activity_logger_path, f"{get_date_string()}_{get_day_of_week_string()}")
        # check if the directory exists, if not create it
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            process_previous_folder()

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