from multiprocessing import Process, Value, Array, Manager
from pynput import keyboard
from pystray import MenuItem, Menu, Icon
from PIL import Image
from threading import Thread
from json import load
from os import chdir
from settings import change_settings_menu
from directkeys import *
from random import uniform

# Goes to the root directory
# (if the program errors when ran (not compiled) try commenting this out,
# some IDE's such as PyCharm automatically set the working dir to the root dir)
chdir("..")

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
    _hotkey = getattr(keyboard.Key, hotkey.value.decode('utf-8'), None)

    if key == _hotkey and running.value == False:
        running.value = True

    elif key == _hotkey and running.value == True:
        running.value = False


def change_settings():
    settings_process = Process(target=change_settings_menu, args=(json_changed,))
    settings_process.start()


# Settings handler. Waits until settings have been marked as changed, then updates via the json file.
def update_settings(settings_dict, click_text, key_text, hotkey_text, json_changed, _exit, click_maximum, click_minimum, press_maximum, press_minimum, profile_text, hotkey):
    while _exit.value:
        if json_changed.value:
            with open('settings.json', 'r') as file:
                main_settings = load(file)
                profile = main_settings['selected_profile']
                profiles = main_settings['profiles']
                profile_path = profiles[profile]
                profile_text.value = f"Profile: {profile}".encode('utf-8')
                with open(profile_path, 'r') as file:
                    settings = load(file)
                    settings_dict["autoclick_delay"] = settings["autoclick_delay"]
                    settings_dict["q_spam_delay"] = settings["key_spam_delay"]
                    click = settings["click"]
                    settings_dict["click"] = globals().get(click.upper(), None)
                    click_text.value = f"Click Type: {click.upper()}".encode('utf-8')

                    _hotkey = settings["hotkey"]
                    hotkey.value = _hotkey.encode('utf-8')
                    hotkey_text.value = f"Hotkey: {_hotkey.upper()}".encode('utf-8')
                    key = settings["key"]
                    key_text.value = f"Key: {key.upper()}".encode("utf-8")

                    click_maximum.value = settings["click_duration_max"]
                    click_minimum.value = settings["click_duration_min"]
                    press_maximum.value = settings["press_duration_max"]
                    press_minimum.value = settings["press_duration_min"]

                    if isinstance(settings["key"], int):
                        integer = integer_names.get(settings["key"])
                        settings_dict["key"] = globals().get(integer, None)
                    else:
                        key_input = settings["key"].upper()
                        if key_input.isdigit():
                            key_name = integer_names.get(int(key_input), None)
                        else:
                            key_name = key_input
                        settings_dict["key"] = globals().get(key_name, None)

                    json_changed.value = False

        sleep(1.5)


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


def trigger_settings_update(icon, item):
    json_changed.value = True


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


# Starts all the threads and subprocesses, and also initialises all the shared variables
if __name__ == "__main__":
    with Manager() as manager:

        settings_changed_bool = Value('b', True)
        running = Value('b', False)
        exit_bool = Value('b', True)
        mode_str = Array('c', b"Autoclicker")
        autoclick_state = Value('b', True)
        hotkey = Array('c', b"         ")

        q_spam_state = Value('b', False)
        d = manager.dict()
        json_changed = Value('b', True)
        click_text = Array('c', b"                    ")
        mode_text = Array('c', b"Mode: Autoclicker")
        key_text = Array('c', b"                    ")
        hotkey_text = Array('c', b"                   ")

        profile_text = Array('c', b"                                     ")

        click_maximum = Value('d', 0.0)
        click_minimum = Value('d', 0.0)
        press_maximum = Value('d', 0.0)
        press_minimum = Value('d', 0.0)

        settings_process = Process(target=update_settings, args=(d, click_text, key_text, hotkey_text, json_changed, exit_bool, click_maximum, click_minimum, press_maximum, press_minimum, profile_text, hotkey,))
        settings_process.start()
        p = Process(target=main, args=(running, exit_bool, mode_str, d, click_maximum, click_minimum, press_maximum, press_minimum,))
        p.start()
        listener = keyboard.Listener(on_press=on_off)
        listener.start()
        tray_thread = Thread(target=tray, args=(click_text, mode_text, key_text, hotkey_text, autoclick_state, q_spam_state, profile_text,))
        tray_thread.start()
        tray_thread.join()
