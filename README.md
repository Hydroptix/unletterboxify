# unletterboxify

Automatically remove annoying black borders from videos

# Why?
Ultrawide monitors are great, especially if you want to fit three windows side by side on a screen. However, many games will add black bars to keep a game at 16:9. Recording software (Shadowplay) picks that up too, so removing those bars automatically would be nice for sharing clips. This script detects those black bars and attempts to remove them without a ton of manual intervention.

# Installation

## Pipenv

`python -m pipenv install`

## Pip

`pip install -r requirements.txt`

# Usage

## Pipenv

### Command Line

`python -m pipenv run unletterboxify.py [filename]`

### BAT file (Windows only)

Drag a video file onto `unletterboxify_pipenv.bat`

## Pip

### Command Line

`python unletterboxify.py [filename]`

### BAT file (Windows only)

Drag a video file onto `unletterboxify_pip.bat`
