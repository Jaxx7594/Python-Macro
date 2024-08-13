# What is this?
A macro made in Python that can reach thousands of clicks/keypresses per second! (Windows only)
# Features
* Ultra-fast
* Support for almost every key and mouse button
* Profiles (quickly swap and save settings to avoid retyping everything!)
* Low-profile (no big clunky GUI, this macro is **accessed via the tray**)
* Randomisable delays (to avoid detection, you can set a minimum and maximum delay between key presses/clicks, and this macro will choose a number in between those two values)
* And more

# Using this macro

You can access this macro's controls **via the icon in the system tray (little arrow on the taskbar in Windows 10/11)**. In there, you'll see 3 rows:

 - **Quit**: Closes the macro upon press
 - **Settings**: Settings can be changed and viewed via this menu. Covered below
 - **Mode**: Modes can be changed via this menu. Covered below

![image](https://github.com/Jaxx7594/Python-Macro/assets/101913901/921977a4-15da-48e4-8acb-25a7659f7dad)

 
## Settings Menu

Settings, when hovered over or clicked, will show 7 more rows:

 - **Profile**: Displays the currently selected profile
 - **Hotkey**: Displays the currently selected hotkey
 - **Mode**: Displays the currently selected mode
 - **Key**: Displays the selected key that will be pressed by the keyspamming mode
 - **Click Type**: Displays the selected type of click (left, middle, right, side buttons) that will be pressed by the autoclicking mode
 - **Change Settings**: Upon click, a settings menu will open. Via this menu, all settings can be changed easily. Covered in more detail below.
 - **Update settings**: Trigger a settings update. You will only need to use this if you manually edit the json files rather than using the settings menu.

 ![image](https://github.com/Jaxx7594/Python-Macro/assets/101913901/97f6afa2-467f-439e-9f17-df75efe67f72)

## Change Settings Menu

Upon press, Change Settings will open a new window. In this window, you'll see an entry for every setting. Most are self-explanatory, but I'll explain a couple that are a bit more interesting:

 - **Duration Minimum/Maximum**: The macro will choose a random number inbetween these 2 values. The chosen number will be how long the key/click is pressed.
 - **Select Profile**: Used to select the profile you want to modify, create or use. You have 2 options, type a profile name into it, or select one from the dropdown. To create a new profile, use option 1 to type the name of your profile (it cannot exist already, otherwise it'll modify rather than create), enter your desired settings, and hit save. To select a profile for usage by the main program, just choose it and hit save.

![image](https://github.com/Jaxx7594/Python-Macro/assets/101913901/50bc3153-6a6c-40db-98d0-093235efc0e5)


## Mode Menu

Mode, when hovered over or clicked, will show 2 more rows:
 - **Key spammer**
 - **Autoclicker**

Clicking 'Key spammer' will set the mode to keyspamming. This means that upon press of the activation hotkey, the macro will spam the currently selected key.

'Autoclicker' does the exact opposite, setting the mode to autoclicking, and clicking with the selected click type upon activation rather than spamming the selected key.

![image](https://github.com/Jaxx7594/Python-Macro/assets/101913901/b02b2ace-1d13-4c57-aea6-c337b44ad48a)


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
nuitka ./src/updater.py --enable-plugin=tk-inter --disable-console --windows-icon-from-ico=./images/icon.png --remove-output --standalone --assume-yes-for-downloads
```
The compiled program can be found at ./main.dist/main.exe
# Todo
* ~~Optimise settings system (can likely handle the settings saving within the settings menu itself, which would save a fair amount of resources)~~ **Done**
* Add more explanatory comments
* General code cleanup
* Possibly remake in a more efficient language such as C++
* Possibly make a Linux version if theres demand for it
