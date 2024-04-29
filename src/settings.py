from tkinter import messagebox

from ttkbootstrap import *
from ttkbootstrap.dialogs.dialogs import Messagebox
from json import dump, load
from pynput.keyboard import Key
from directkeys import *
from os import remove

# Define global variables
hotkey_entry = None
autoclick_delay_entry = None
key_spam_delay_entry = None
key_entry = None
click_entry = None
click_type = None
click_max_entry = None
click_min_entry = None
key_max_entry = None
key_min_entry = None

successful = False

click_types = ['', 'LBUTTON', 'RBUTTON', 'MBUTTON', 'XBUTTON1', 'XBUTTON2']

def validate(show_messages=True):
    global hotkey_entry, autoclick_delay_entry, key_spam_delay_entry, key_entry, click_type, click_max_entry, click_min_entry, key_max_entry, key_min_entry

    error = False
    value_error = False

    # Retrieve values from entry fields
    click = click_type.get()
    click_max = click_max_entry.get()
    click_min = click_min_entry.get()
    hotkey = hotkey_entry.get()
    key = key_entry.get()
    key_max = key_max_entry.get()
    key_min = key_min_entry.get()
    autoclick_delay = autoclick_delay_entry.get()
    key_spam_delay = key_spam_delay_entry.get()

    def err(title, message):
        if show_messages:
            Messagebox.show_error(title=title, message=message)

    # Validate settings
    for setting, value in {
        "Autoclick delay": autoclick_delay,
        "Key spam delay": key_spam_delay,
        "Click duration minimum": click_min,
        "Click duration maximum": click_max,
        "Keypress duration minimum": key_min,
        "Keypress duration maximum": key_max
    }.items():
        try:
            value = float(value)
            if value < 0:
                err(title='Error', message=f"{setting} cannot be negative.")
                error = True
        except ValueError:
            err(title='Error', message=f"{setting} must be a valid number.")
            value_error = True

    if value_error:
        return

    try:
        click_min = float(click_min)
        click_max = float(click_max)
        key_min = float(key_min)
        key_max = float(key_max)
        if click_max < click_min:
            err(title="Error", message="Click duration maximum must be greater than or equal to minimum.")
            error = True
        if key_max < key_min:
            err(title="Error", message="Keypress duration maximum must be greater than or equal to minimum.")
            error = True
    except ValueError as e:
        err(title='Error', message=str(e))
        error = True

    if not hasattr(Key, hotkey):
        err(title='Error', message='Invalid hotkey.')
        error = True

    if key.isdigit():
        integer = integer_names.get(int(key), None)
        if integer == None or key == None:
            err(title='Error',
                message='Invalid key. Looks like you entered an invalid number. The key entry only accepts digits, e.g. 0, 5, 3, etc.')
            error = True
    else:
        _key = globals().get(key.upper(), None)
        if _key == None:
            err(title='Error',
                message="Invalid key. Looks like you entered an invalid key. The key entry only accepts the letters of the alphabet, and special keys such as f6, alt, ctrl, etc. Generally, if it isn't on your keyboard, its invalid.")
            error = True

    if click not in click_types or click == '':
        err(title='Error', message='Invalid click type.')
        error = True

    if error:
        return False


    autoclick_delay = float(autoclick_delay)
    key_spam_delay = float(key_spam_delay)

    if autoclick_delay < 0.00025 or key_spam_delay < 0.00025:
        Messagebox.show_warning(title='Warning', message='Delays below 0.00025 are likely to crash programs and low end devices due to its sheer speed. Proceed with caution.')

    # Save settings to JSON file
    settings = {
        "hotkey": hotkey,
        "autoclick_delay": autoclick_delay,
        "key_spam_delay": key_spam_delay,
        "key": key,
        "click": click,
        "click_duration_max": float(click_max),
        "click_duration_min": float(click_min),
        "press_duration_max": float(key_max),
        "press_duration_min": float(key_min)
    }
    return settings

# Checks if settings entered are valid. If they aren't, it shows an error to the user and doesn't modify the json file,
# If they are, it dumps it in the json file and sets a shared var to tell the settings updater in main.py to update.
def save_settings(json_changed, profile_var):

    settings = validate()
    if settings == False:
        return

    with open('settings.json', 'r+') as file:
        main_settings = load(file)
        main_settings['selected_profile'] = profile_var.get().lower()
        profile = main_settings['selected_profile']
        profiles = main_settings['profiles']
        if main_settings['selected_profile'] not in profiles:
            main_settings['profiles'][profile] = f"profiles/{profile}.json"
        profile_path = profiles[profile]

        file.seek(0)
        file.truncate()
        dump(main_settings, file, indent=4)

        with open(profile_path, 'w') as file:
            dump(settings, file, indent=4)
    json_changed.value = True
    Messagebox.show_info(title='Message', message='Settings saved successfully.')
    return True


# Starts the tkinter GUI for changing settings. Just a simple json frontend for the non tech nerds basically.
def change_settings_menu(json_changed):
    global hotkey_entry, autoclick_delay_entry, key_spam_delay_entry, key_entry, click_type, click_max_entry, click_min_entry, key_max_entry, key_min_entry, successful

    root = Window()
    root.style.theme_use('darkly')
    root.title('Settings')
    icon = PhotoImage(file=r"images/icon.png")
    root.iconphoto(False, icon)
    root.resizable(False, False)

    def on_close():
        if saving_needed():
            Messagebox.show_error(title='Error', message='Please save before closing.')
        else:
            root.destroy()

    root.protocol('WM_DELETE_WINDOW', on_close)

    click_type = StringVar(root)
    profile_var = StringVar(root)

    # Create labels and entry fields for each setting
    labels_entries = [
        ("Hotkey:", hotkey_entry),
        ("Autoclick Delay:", autoclick_delay_entry),
        ("Click Duration Minimum:", click_min_entry),
        ("Click Duration Maximum:", click_max_entry),
        ("Key Spam Delay:", key_spam_delay_entry),
        ("Keypress Duration Minimum:", key_min_entry),
        ("Keypress Duration Maximum:", key_max_entry),
        ("Key:", key_entry)
    ]

    for i, (label_text, entry_var) in enumerate(labels_entries):
        Label(root, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        entry_var = Entry(root)
        entry_var.grid(row=i, column=1, padx=10, pady=5)

        # Assign the correct entry variables to global variables
        if label_text == "Hotkey:":
            hotkey_entry = entry_var
        elif label_text == "Autoclick Delay:":
            autoclick_delay_entry = entry_var
        elif label_text == "Click Duration Minimum:":
            click_min_entry = entry_var
        elif label_text == "Click Duration Maximum:":
            click_max_entry = entry_var
        elif label_text == "Key Spam Delay:":
            key_spam_delay_entry = entry_var
        elif label_text == "Keypress Duration Minimum:":
            key_min_entry = entry_var
        elif label_text == "Keypress Duration Maximum:":
            key_max_entry = entry_var
        elif label_text == "Key:":
            key_entry = entry_var

    # Create dropdown menu for click types
    Label(root, text='Click type:').grid(row=8, column=0, padx=10, pady=5, sticky='w')
    click_menu = OptionMenu(root, click_type, *click_types)
    click_menu.grid(row=8, column=1, padx=10, pady=5)
    click_menu.config(width=16)

    def delete_profile():
        with open('settings.json', 'r+') as file:
            main_settings = load(file)
            remove(main_settings['profiles'][profile_var.get()])
            del main_settings['profiles'][profile_var.get()]
            file.seek(0)
            file.truncate()
            dump(main_settings, file, indent=4)
        profile_var.set('')

    delete_profile_button = Button(root, text='Delete Profile', command=delete_profile, width=19)

    # Function to update settings when profile is changed
    def update_settings(profile):
        profile = profile.lower()
        update_profile_vars()
        if profile in profiles:
            profile_path = profiles[profile]
            with open(profile_path, 'r') as file:
                settings = load(file)
                for entry_var, setting_key in zip(
                        [hotkey_entry, autoclick_delay_entry, click_min_entry, click_max_entry, key_spam_delay_entry,
                         key_min_entry, key_max_entry, key_entry],
                        ["hotkey", "autoclick_delay", "click_duration_min", "click_duration_max", "key_spam_delay",
                         "press_duration_min", "press_duration_max", "key"]):
                    entry_var.delete(0, END)
                    entry_var.insert(0, settings.get(setting_key, ''))
                click_type.set(settings.get('click', ''))

                delete_profile_button.grid(row=10, column=1, pady=10)
        else:
            for entry_var, setting_key in zip(
                    [hotkey_entry, autoclick_delay_entry, click_min_entry, click_max_entry, key_spam_delay_entry,
                     key_min_entry, key_max_entry, key_entry],
                    ["hotkey", "autoclick_delay", "click_duration_min", "click_duration_max", "key_spam_delay",
                     "press_duration_min", "press_duration_max", "key"]):
                entry_var.delete(0, END)
            click_type.set('')

            delete_profile_button.grid_forget()

    def on_profile_change(*args):
        selected_profile = profile_var.get()
        update_settings(selected_profile)

    profile_var.trace_add('write', on_profile_change)

    def update_profile_vars():
        with open('settings.json', 'r') as file:
            global profiles, profile_names
            main_settings = load(file)
            profiles = main_settings.get('profiles', {})
            profile_names = list(profiles.keys())
            try:
                profile_menu['values'] = profile_names
            except:
                return

    # Load profiles from JSON file
    try:
        update_profile_vars()
        with open('settings.json', 'r') as file:
            profile_var.set(load(file)['selected_profile'].lower())

        # Dropdown menu for profile selection
        Label(root, text='Select Profile:').grid(row=9, column=0, padx=10, pady=5, sticky='w')
        profile_menu = Combobox(root, textvariable=profile_var, values=profile_names)
        profile_menu.grid(row=9, column=1, padx=10, pady=5)
        profile_menu.config(width=18)

    except FileNotFoundError:
        pass

    def saving_needed():

        settings = validate(show_messages=False)
        if settings == False:
            return True

        with open('settings.json', 'r') as file:
            main_settings = load(file)

            try:
                selected_profile = main_settings.get('selected_profile')
                profile_dir = main_settings['profiles'][selected_profile]
            except:
                return True

            with open(profile_dir, 'r') as file:
                if load(file) == settings and selected_profile == profile_var.get():
                    return False
                else:
                    return True

    def _save_settings(json_changed, profile_var):
        global successful
        if profile_var.get() == '':
            Messagebox.show_error('Please select or create a profile and try again.', 'Error')
            return
        successful = save_settings(json_changed, profile_var)
        if not successful:
            return
        update_settings(profile_var.get())

    # Button to save settings
    update_button = Button(root, text='Save Profile', command=lambda: _save_settings(json_changed, profile_var), width=19)
    update_button.grid(row=10, column=0, pady=10)

    root.mainloop()
