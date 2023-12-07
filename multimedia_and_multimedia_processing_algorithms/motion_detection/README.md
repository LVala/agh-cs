# Simple motion detection system in OpenCV
### 2021/22 summer semester, Computer Science WIEiT AGH UST

This repository contains our 1st project for Multimedia and Multimedia Processing Algorithms Course.

#### How to setup the project for development:
- Make sure you have [Python 3 and pip](https://www.python.org/downloads/) installed (3.10 or later)
- Clone this repository
- Create and activate virtual environment with [venv](https://docs.python.org/3/library/venv.html)
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate  # on Linux
```
- Install dependencies with 
```bash
$ pip install -r requirements.txt
```

#### Features:
- the ability to set the video source
- real time video preview
- selection of the area (mask) where the motion detection will work
- visual confirmation of detected motion
- the ability to set the motion detection sensitivity
- debug mode (visualization of the following stages of image processing)

#### Authors:
- Monika Pyrek
- Dominika Bocheńczyk
- Łukasz Wala