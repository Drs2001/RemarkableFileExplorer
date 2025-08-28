## Remarkable File Explorer
A GUI application meant to interface with remarkable tablets and allow for a much easier to use and less laggy interface than the default web UI provided for local access.

## Build from Scratch

### Virtual Environment Setup
The pyproject.toml and uv.lock files are already provided so simple run 'uv sync' to initialize the project and create your virtual environment. Alternativally a requirements.txt file is provided if you'd like to use something else like conda.

### Running
Once your virtual environment is setup with dependencies installed simply run the main.py file in the root directory. *Note: The program will take a second to launch if a remarkable tablet isn't plugged in as during initialization it tries to establish a connection and if it can't it will take longer, so plug in your tablet and enable USB connection before launching.

### Building
This projects .exe is build with pyinstaller, so simply run 'pyinstaller main.spec' to build the executable

## Disclaimer
While no issues came up in testing use program at your own risk! The application owner is not responsible for any file or data loss!

## Credit
Icons: https://www.iconarchive.com/artist/hopstarter.html
