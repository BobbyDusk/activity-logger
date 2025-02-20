# Activity Logger

<img src="logo.png" alt="Logo" width="200" />

Takes periodic screenshot to help you track your activity

Only works on linux.

## Note

On gnome-wayland a flash appears whenever a screenshot is taken. You can disable this by disabling animations in the accessibility menu.

## Stack

- python
- systemd
- uv

## TODO

- automatic backups

## TODO (done)

- detect completely black screens and remove them, since those indicate when computer was sleeping, so should be treated as stop
- On start/stop cards, also mention how much time since last start/stop
- For every day, also have a json file with a summary of
  - start/stop times (both in real life as well as video timestamp)
  - total time on computer
- csv file for every day with blocks
- Add chapters for start-stop see [here](https://medium.com/@dathanbennett/adding-chapters-to-an-mp4-file-using-ffmpeg-5e43df269687) and [here](https://ikyle.me/blog/2020/add-mp4-chapters-ffmpeg)


