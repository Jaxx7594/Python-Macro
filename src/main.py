import sys
from multiprocessing import Process, Value, Array, Manager
from subprocess import Popen, CREATE_NEW_CONSOLE
from pynput import keyboard
from pystray import MenuItem, Menu, Icon
from PIL import Image
from threading import Thread
from os import chdir, path
from settings import change_settings_menu, set_settings
from directkeys import *
from updater import *
from random import uniform
from ctypes import windll, c_void_p, c_bool, c_wchar_p
from json import load, dump
from ttkbootstrap.dialogs.dialogs import Messagebox
from windows_toasts import Toast, ToastDisplayImage, WindowsToaster
import ttkbootstrap as ttk
import requests

import winrt.windows.foundation.collections # This is simply to ensure Nuitka realises this is a requirement.


def toast(text):
    toaster = WindowsToaster('Macro')

    toast = Toast()
    toast.text_fields = [text]
    # str or PathLike
    toast.AddImage(ToastDisplayImage.fromPath('./images/icon.png'))

    toaster.show_toast(toast)

def internet_connected():
    try:
        requests.get("https://github.com", timeout=8)
        return True
    except requests.ConnectionError:
        return False


# Tried to keep this as fast as possible. All vars are initialised before activation so that no precious cpu cycles are
# spent asking multiprocessing for a var, and instead firing off clicks/key presses
def main(r, exit_b, mode, settings, click_maximum, click_minimum, press_maximum, press_minimum):
    while exit_b.value:
        sleep(0.35)
        autoclick_delay = settings["autoclick_delay"]
        key_spam_delay = settings["q_spam_delay"]
        key = settings["key"]
        click = settings["click"]

        click_min = click_minimum.value
        click_max = click_maximum.value
        press_min = press_minimum.value
        press_max = press_maximum.value

        autoclicker = True if mode.value == b"Autoclicker" else None
        while r.value:
            if autoclicker:
                ClickMouse(click, duration=duration(click_min, click_max))
                sleep(autoclick_delay)
            else:
                PressKey(key, duration=duration(press_min, press_max))
                sleep(key_spam_delay)


# Seems random num generating is pretty slow, so this is more performant
def duration(_min, _max):
    if _max != _min:
        return uniform(_min, _max)
    return _min


# Hotkey handler (activates/deactivates when hotkey is pressed)
def on_off(key):
    global running
    global hotkey
    global mode_switch_hotkey
    _hotkey = getattr(keyboard.Key, hotkey.value.decode('utf-8'), None)
    _mode_switch_hotkey = getattr(keyboard.Key, mode_switch_hotkey.value.decode('utf-8'), None)

    if key == _hotkey and running.value == False:
        running.value = True

    elif key == _hotkey and running.value == True:
        running.value = False

    elif key == _mode_switch_hotkey:
        if not running.value:
            if mode_str.value.decode('utf-8') == "Autoclicker":
                q_spam_state.value = True
                autoclick_state.value = not q_spam_state.value
                mode_str.value = "Key Spammer".encode('utf-8')
            else:
                autoclick_state.value = True
                q_spam_state.value = not autoclick_state.value
                mode_str.value = "Autoclicker".encode('utf-8')

            toast(f"Changed mode: {mode_str.value.decode('utf-8')}")
        else:
            toast('Cannot change mode whilst running.')

# Opens the settings menu.
def change_settings():
    settings_process = Process(target=change_settings_menu, args=(first_time_running, d, click_text, key_text, hotkey_text, click_maximum, click_minimum, press_maximum, press_minimum, profile_text, hotkey, mode_switch_hotkey,))
    settings_process.start()


# Terminates all threads/subprocesses by setting exit_bool to False. Any thread/subprocess with a while loop checks if
# exit_bool = False, and if it is, it returns. Without any threads/subprocesses to hold back the main thread, it exits.
def quit_window(icon, item):
    global exit_bool
    icon.stop()
    exit_bool.value = False


# Changes the mode, pretty self-explanatory.
def change_mode(icon, item, q_spam_state, autoclick_state):
    mode_str.value = item.text.encode('utf-8')
    mode_text.value = f"Mode: {item.text}".encode('utf-8')
    if item.text == "Autoclicker":
        autoclick_state.value = not item.checked
        q_spam_state.value = not autoclick_state.value
    else:
        q_spam_state.value = not item.checked
        autoclick_state.value = not q_spam_state.value


# Only purpose of this is to repeatedly update the tray menu, since it seems the tray only does it itself when a
# MenuItem is clicked, so when one isn't, simply nothing updates so out of date settings used to be displayed.
def update_menu(icon, _exit):
    while _exit.value:
        sleep(1)
        icon.update_menu()

# Updates settings. This is activated via a tray button.
# Only needed if the user changes json files directly rather than using the settings menu.
def trigger_settings_update(icon, item):
    set_settings(d, click_text, key_text, hotkey_text, click_maximum, click_minimum, press_maximum, press_minimum, profile_text, hotkey, mode_switch_hotkey)


# Tray menu. I don't think a simple macro should need a full on GUI, so I settled on a tray application.
def tray(click_text, mode_text, key_text, hotkey_text, autoclick_state, q_spam_state, profile_text):
    image = Image.open("images/icon.png")
    menu = (
        MenuItem('Quit', quit_window),
        MenuItem('Settings',
                 Menu(
                     MenuItem(lambda text: str(profile_text.value, 'utf-8'), None, enabled=False),
                     Menu.SEPARATOR,
                     MenuItem(lambda text: str(hotkey_text.value, 'utf-8'), None, enabled=False),
                     MenuItem(lambda text: str(mode_text.value, 'utf-8'), None, enabled=False),
                     MenuItem(lambda text: str(key_text.value, 'utf-8'), None, enabled=False),
                     MenuItem(lambda text: str(click_text.value, 'utf-8'), None, enabled=False),
                     MenuItem('Change Settings', change_settings),
                     MenuItem('Update Settings', trigger_settings_update),
                 ),
                 ),
        MenuItem('Mode',
                 Menu(
                     MenuItem("Key spammer", lambda icon, item: change_mode(icon, item, q_spam_state, autoclick_state), checked=lambda item: q_spam_state.value),
                     MenuItem("Autoclicker", lambda icon, item: change_mode(icon, item, q_spam_state, autoclick_state), checked=lambda item: autoclick_state.value),
                 ),
                 )
    )
    icon = Icon("name", image, "Macro", menu)
    update_thread = Thread(target=update_menu, args=(icon, exit_bool,))
    update_thread.start()
    icon.run()


def is_another_instance_running():
    # Define the CreateMutexW function
    CreateMutexW = windll.kernel32.CreateMutexW
    CreateMutexW.argtypes = [c_void_p, c_bool, c_wchar_p]
    CreateMutexW.restype = c_void_p

    # Create a named mutex
    mutex_name = "PythonMacro mutex"
    handle = CreateMutexW(None, False, mutex_name)

    # Check if the mutex already exists
    ERROR_ALREADY_EXISTS = 183
    if ctypes.windll.kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
        return True
    return False

# Starts all the threads and subprocesses, and also initialises all the shared variables
if __name__ == "__main__":

    # Sets working dir to root dir.
    chdir(path.dirname(path.abspath(__file__)))
    chdir('..')

    if not internet_connected():
        root = ttk.Window()
        root.style.theme_use('darkly')
        Messagebox.show_error(title='Internet not connected',
                              message='It seems you do not currently have an internet connection, so this macro will not be able to check for updates. You can still use it though.')
        root.destroy()
    # Checks for updates, and if there is an update available, starts the updater and exits.
    elif new_version_available("Jaxx7594", "Python-Macro", load(open('settings.json', 'r'))):

        root = ttk.Window()
        root.style.theme_use('darkly')
        result = Messagebox.show_question(title='Update available', message='There is a new update available. Would you like to update now?', buttons=["No:secondary", "Yes:primary"])
        root.destroy()

        if result == "Yes":

            download_latest_release('Jaxx7594', 'Python-Macro')

            if path.basename(path.dirname(path.abspath(__file__))) == "main.dist":
                try:
                    extract_specific_directory(zip_file, 'Macro/updater.dist', './updater.dist')
                except Exception as error:
                    root = ttk.Window()
                    root.style.theme_use('darkly')
                    Messagebox.show_error(title='Update failed',
                                          message=f'We failed to update the updater. The update cannot continue, as using an old updater version may cause problems. Please report this to the Github repository. The macro will now terminate.\n Specific error:\n{error}')
                    root.destroy()
                    exit()

                Popen(['updater.dist\\updater.exe'], shell=True, creationflags=CREATE_NEW_CONSOLE)
                exit()

            else:

                try:
                    extract_specific_file(zip_file, 'Macro/src/updater.py', './src/updater.py')
                except Exception as error:
                    root = ttk.Window()
                    root.style.theme_use('darkly')
                    Messagebox.show_error(title='Update failed', message=f'We failed to update the updater. The update cannot continue, as using an old updater version may cause problems. Please report this to the Github repository. Seeing as you\'re likely a developer, please provide proper debug information. The macro will now terminate. \n Specific error:\n{error}')
                    root.destroy()
                    exit()

                Popen(['pythonw', 'src\\updater.py'], creationflags=CREATE_NEW_CONSOLE)
                exit()

    if is_another_instance_running():
        if load(open('settings.json', 'r'))['show_multiple_instances_error']:
            root = ttk.Window()
            root.style.theme_use('darkly')
            result = Messagebox.show_question(title='Already running!', message='This macro is already running! You cannot have multiple instances of this macro running at the same time. You can find the controls of the currently running instance in the system tray. ', buttons=["Don't Show Again:secondary", "Ok:primary"])
            root.destroy()
            if result == "Don't Show Again":
                with open('settings.json', 'r+') as file:
                    settings = load(file)
                    settings['show_multiple_instances_error'] = False

                    file.seek(0)
                    file.truncate()
                    dump(settings, file, indent=4)
        sys.exit()

    with Manager() as manager:


        running = Value('b', False)
        exit_bool = Value('b', True)
        mode_str = Array('c', b"Autoclicker")
        autoclick_state = Value('b', True)
        hotkey = Array('c', b"         ")
        mode_switch_hotkey = Array('c', b"         ")

        q_spam_state = Value('b', False)
        d = manager.dict()
        first_time_running = Value('b', 2)
        click_text = Array('c', b"                    ")
        mode_text = Array('c', b"Mode: Autoclicker")
        key_text = Array('c', b"                    ")
        hotkey_text = Array('c', b"                   ")

        profile_text = Array('c', b"                                     ")

        click_maximum = Value('d', 0.0)
        click_minimum = Value('d', 0.0)
        press_maximum = Value('d', 0.0)
        press_minimum = Value('d', 0.0)

        settings_process = Process(target=set_settings, args=(d, click_text, key_text, hotkey_text, click_maximum, click_minimum, press_maximum, press_minimum, profile_text, hotkey, mode_switch_hotkey, first_time_running))
        settings_process.start()
        p = Process(target=main, args=(running, exit_bool, mode_str, d, click_maximum, click_minimum, press_maximum, press_minimum,))
        p.start()
        listener = keyboard.Listener(on_press=on_off)
        listener.start()
        tray_thread = Thread(target=tray, args=(click_text, mode_text, key_text, hotkey_text, autoclick_state, q_spam_state, profile_text,))
        tray_thread.start()

        while first_time_running.value == 2:
            sleep(0.1)

        if first_time_running.value:
            change_settings()

        tray_thread.join()
