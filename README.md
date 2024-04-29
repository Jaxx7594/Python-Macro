# What is this?
A macro made in Python that can reach thousands of clicks/keypresses per second! (Windows only)
# Features
* Ultra-fast
* Support for almost every key and mouse button
* Profiles (quickly swap and save settings to avoid retyping everything!)
* Low-profile (no big clunky GUI, this macro is accessed via the tray)
* Randomisable delays (to avoid detection, you can set a minimum and maximum delay between key presses/clicks, and this macro will choose a number in between those two values)
* And more
# Building from source
**1.** Clone the repo:
```console
git clone https://github.com/Jaxx7594/Python-Macro.git
```
**2.** Install required modules:
```console
cd Python-Macro
python -m pip install -r requirements.txt
```
**3.** Build:
```console
nuitka ./src/main.py --enable-plugin=tk-inter --disable-console --windows-icon-from-ico=./images/icon.png --remove-output --standalone --assume-yes-for-downloads
```
The compiled program can be found at ./main.dist/main.exe
# Todo
* Optimise settings system (can likely handle the settings saving within the settings menu itself, which would save a fair amount of resources)
* Possibly remake in a more efficient language such as C++
* Possibly make a Linux version if theres demand for it
