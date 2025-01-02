from pathlib import Path
import datetime
import pyscreenshot as ImageGrab
from PIL import Image, ImageDraw, ImageFont
import subprocess
import re


activity_logger_path = Path(Path.home(), "activity_logger")
font_path = Path(activity_logger_path, ".src/Arial.ttf")
FPS = 2
DURATION_DISPLAY_CARDS = 3  # in seconds
frames_display_cards = round(FPS * DURATION_DISPLAY_CARDS)


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
    pattern = r"^\d{4}-\d{2}-\d{2}"
    return bool(re.match(pattern, date_string))


def create_video_from_images_in_folder(folder_path: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-framerate",
            f"{FPS}",
            "-pattern_type",
            "glob",
            "-i",
            f"{folder_path}/*.jpg",
            "-vcodec",
            "libx265",
            "-y",
            f"{folder_path}/video.mp4",
        ]
    )


def check_if_video_exists(folder_path: Path) -> bool:
    return Path(folder_path, "video.mp4").exists()


def list_directories(folder_path: Path) -> list:
    dirs = [
        p.name for p in folder_path.iterdir() if p.is_dir() and check_if_date(p.name)
    ]
    return sorted(dirs)


def get_previous_folder_path() -> Path:
    directories = list_directories(activity_logger_path)
    if len(directories) >= 2:
        newest_folder = directories[-2]
        return Path(activity_logger_path, newest_folder)
    else:
        return None


def create_text_image(header: str, body: list[str]) -> Image:
    image = Image.new("RGB", (1920, 1080), color="black")
    draw = ImageDraw.Draw(image)
    font_size = 42
    font = ImageFont.truetype(font_path, font_size)
    font_size_header = 82
    font_header = ImageFont.truetype(font_path, font_size_header)
    total_height = font_size_header + font_size * len(body)
    text_color = "white"
    gap = 16

    # draw header
    text_width = draw.textlength(header, font=font_header)
    y = image.height // 2 - total_height // 2
    x = image.width // 2 - text_width // 2
    draw.text((x, y), header, font=font_header, fill=text_color)

    # draw strings
    for i, line in enumerate(body):
        text_width = draw.textlength(line, font=font)
        y = (
            image.height // 2
            - total_height // 2
            + i * (font_size + gap)
            + (font_size_header + gap)
            + gap
        )
        x = image.width // 2 - text_width // 2
        position = (x, y)
        draw.text(position, line, font=font, fill=text_color)
    return image


def get_base_card_text(
    start_time: datetime.datetime, stop_time: datetime.datetime
) -> list[str]:
    return [
        f"from {get_time_string_from_date(start_time)}",
        f"to {get_time_string_from_date(stop_time)}",
        f"duration: {stop_time - start_time}",
    ]


def save_card(image, folder_path, base_name):
    for i in range(frames_display_cards):
        image_path = Path(folder_path, f"{base_name}_{i}.jpg")
        image.save(image_path)


def process_start_time(
    start_time: datetime.datetime, stop_time: datetime.datetime, folder_path: Path
) -> None:
    image = create_text_image("START", get_base_card_text(start_time, stop_time))
    save_card(
        image,
        folder_path,
        f"{get_date_time_string_from_date(start_time - datetime.timedelta(minutes=1))}_START",
    )


def process_stop_time(
    start_time: datetime.datetime, stop_time: datetime.datetime, folder_path: Path
) -> None:
    image = create_text_image("STOP", get_base_card_text(start_time, stop_time))
    save_card(
        image,
        folder_path,
        f"{get_date_time_string_from_date(stop_time + datetime.timedelta(minutes=1))}_STOP",
    )


def get_files_in_folder(folder_path: Path) -> list[Path]:
    return sorted(list(folder_path.glob("*.jpg")))


def insert_start_stop_images(folder_path: Path) -> None:
    files = get_files_in_folder(folder_path)
    previous_date_time = None
    time_blocks = []

    def add_start(time, index):
        time_blocks.append(
            {
                "start_time": time,
                "start_index": index,
                "start_timestamp": datetime.timedelta(
                    seconds=(
                        (index + 2 * frames_display_cards * len(time_blocks)) / FPS
                    )
                ),
            }
        )

    def add_stop(time, index):
        time_blocks[-1]["stop_time"] = time
        time_blocks[-1]["stop_index"] = index
        time_blocks[-1]["stop_timestamp"] = datetime.timedelta(
            seconds=(((index + 1) + 2 * frames_display_cards * len(time_blocks)) / FPS)
        )

    for index, image_path in enumerate(files):
        date_time = datetime.datetime.strptime(image_path.stem, "%Y-%m-%d_%H:%M:%S")
        if index == 0:
            add_start(date_time, index)
        elif index == len(files) - 1:
            add_stop(date_time, index)
        elif date_time - previous_date_time >= datetime.timedelta(minutes=10):
            add_stop(previous_date_time, index - 1)
            add_start(date_time, index)
        previous_date_time = date_time

    summary_body = []
    for index, time_block in enumerate(time_blocks):
        summary_body.append(
            f"block {index + 1}: {get_time_string_from_date(time_block.get('start_time'))} - {get_time_string_from_date(time_block.get('stop_time'))} ({time_block.get('stop_time') - time_block.get('start_time')})"
        )
    total_duration_seconds = sum(
        [
            (time_block.get("stop_time") - time_block.get("start_time")).total_seconds()
            for time_block in time_blocks
        ]
    )
    total_duration = datetime.timedelta(seconds=total_duration_seconds)
    summary_body.append("—————————————————")
    summary_body.append(f"Total time: {total_duration}")
    image = create_text_image("Summary", summary_body)
    time_string = get_date_time_string_from_date(
        time_blocks[0].get("start_time") - datetime.timedelta(minutes=2)
    )
    base_name = f"{time_string}_SUMMARY"
    save_card(image, folder_path, base_name)
    # All timestaps need to be increased because of summary
    for i in range(len(time_blocks)):
        time_blocks[i]["start_timestamp"] = time_blocks[i][
            "start_timestamp"
        ] + datetime.timedelta(seconds=frames_display_cards / FPS)
        time_blocks[i]["stop_timestamp"] = time_blocks[i][
            "stop_timestamp"
        ] + datetime.timedelta(seconds=frames_display_cards / FPS)

    for time_block in time_blocks:
        process_start_time(
            time_block.get("start_time"), time_block.get("stop_time"), folder_path
        )
        process_stop_time(
            time_block.get("start_time"), time_block.get("stop_time"), folder_path
        )


# Completely black images indicate that the computer was sleeping,
# so should be treated as stop
def remove_black_images(folder_path: Path) -> None:
    files = get_files_in_folder(folder_path)
    files_to_remove = []
    for image_path in files:
        if check_if_image_is_black(image_path):
            files_to_remove.append(image_path)
    for file_path in files_to_remove:
        Path(file_path).unlink()


def check_if_image_is_black(image_path: Path) -> bool:
    image = Image.open(image_path)
    grayscale_image = image.convert("L")
    histogram = grayscale_image.histogram()
    pixels = sum(histogram)
    black_pixels = histogram[0]
    black_percentage = black_pixels / pixels
    return black_percentage > 0.97


def move_video_and_remove_folder(folder_path: Path) -> None:
    video_path = Path(folder_path, "video.mp4")
    new_video_path = Path(activity_logger_path, f"{folder_path.name}.mp4")
    video_path.rename(new_video_path)
    # subprocess.run(["rm", "-rf", folder_path])


def process_folder(folder_path: Path) -> None:
    if folder_path:
        remove_black_images(folder_path)
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
        dir_path = Path(
            activity_logger_path, f"{get_date_string()}_{get_day_of_week_string()}"
        )
        # check if the directory exists, if not create it
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            previous_folder_path = get_previous_folder_path()
            process_folder(previous_folder_path)

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
    # run()
    folder_path = Path("./2025-01-02_Thursday")
    process_folder(folder_path)
