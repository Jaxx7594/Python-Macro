# All credit goes to: https://gist.github.com/Aniruddha-Tapas/1627257344780e5429b10bc92eb2f52a
# Great code, saved me the effort of figuring out the Windows API. Made a few changes, but mostly their code.

# directkeys.py
# http://stackoverflow.com/questions/13564851/generate-keyboard-events
# msdn.microsoft.com/en-us/library/dd375731

import ctypes
from ctypes import wintypes
from time import sleep

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

MAPVK_VK_TO_VSC = 0

# List of all codes for keys:
# # msdn.microsoft.com/en-us/library/dd375731

LBUTTON = 0x0002  # Left mouse button
RBUTTON = 0x0008  # Right mouse button
MBUTTON = 0x0020  # Middle mouse button (three-button mouse)
XBUTTON1 = 0x05  # X1 mouse button
XBUTTON2 = 0x06  # X2 mouse button

CANCEL = 0x03  # Control-break processing
BACK = 0x08  # BACKSPACE key
TAB = 0x09  # TAB key
CLEAR = 0x0C  # CLEAR key
RETURN = 0x0D  # ENTER key
SHIFT = 0x10  # SHIFT key
CONTROL = 0x11  # CTRL key
MENU = 0x12  # ALT key
PAUSE = 0x13  # PAUSE key
CAPITAL = 0x14  # CAPS LOCK key
KANA = 0x15  # IME Kana mode
HANGUEL = 0x15  # IME Hanguel mode (maintained for compatibility; use HANGUL)
HANGUL = 0x15  # IME Hangul mode
JUNJA = 0x17  # IME Junja mode
FINAL = 0x18  # IME final mode
HANJA = 0x19  # IME Hanja mode
KANJI = 0x19  # IME Kanji mode
ESCAPE = 0x1B  # ESC key
CONVERT = 0x1C  # IME convert
NONCONVERT = 0x1D  # IME nonconvert
ACCEPT = 0x1E  # IME accept
MODECHANGE = 0x1F  # IME mode change request
SPACE = 0x20  # SPACEBAR
PRIOR = 0x21  # PAGE UP key
NEXT = 0x22  # PAGE DOWN key
END = 0x23  # END key
HOME = 0x24  # HOME key
LEFT = 0x25  # LEFT ARROW key
UP = 0x26  # UP ARROW key
RIGHT = 0x27  # RIGHT ARROW key
DOWN = 0x28  # DOWN ARROW key
SELECT = 0x29  # SELECT key
PRINT = 0x2A  # PRINT key
EXECUTE = 0x2B  # EXECUTE key
SNAPSHOT = 0x2C  # PRINT SCREEN key
INSERT = 0x2D  # INS key
DELETE = 0x2E  # DEL key
HELP = 0x2F  # HELP key

integer_names = {
    0: "ZERO",
    1: "ONE",
    2: "TWO",
    3: "THREE",
    4: "FOUR",
    5: "FIVE",
    6: "SIX",
    7: "SEVEN",
    8: "EIGHT",
    9: "NINE",
    "0": "ZERO",
    "1": "ONE",
    "2": "TWO",
    "3": "THREE",
    "4": "FOUR",
    "5": "FIVE",
    "6": "SIX",
    "7": "SEVEN",
    "8": "EIGHT",
    "9": "NINE"
}

ZERO = 0x30  # 0 key
ONE = 0x31  # 1 key
TWO = 0x32  # 2 key
THREE = 0x33  # 3 key
FOUR = 0x34  # 4 key
FIVE = 0x35  # 5 key
SIX = 0x36  # 6 key
SEVEN = 0x37  # 7 key
EIGHT = 0x38  # 8 key
NINE = 0x39  # 9 key

A = 0x41
B = 0x42
C = 0x43
D = 0x44
E = 0x45
F = 0x46
G = 0x47
H = 0x48
I = 0x49
J = 0x4A
K = 0x4B
L = 0x4C
M = 0x4D
N = 0x4E
O = 0x4F
P = 0x50
Q = 0x51
R = 0x52
S = 0x53
T = 0x54
U = 0x55
V = 0x56
W = 0x57
X = 0x58
Y = 0x59
Z = 0x5A
LWIN = 0x5B  # Left Windows key (Natural keyboard)
RWIN = 0x5C  # Right Windows key (Natural keyboard)
APPS = 0x5D  # Applications key (Natural keyboard)
SLEEP = 0x5F  # Computer Sleep key
NUMPAD0 = 0x60  # Numeric keypad 0 key
NUMPAD1 = 0x61  # Numeric keypad 1 key
NUMPAD2 = 0x62  # Numeric keypad 2 key
NUMPAD3 = 0x63  # Numeric keypad 3 key
NUMPAD4 = 0x64  # Numeric keypad 4 key
NUMPAD5 = 0x65  # Numeric keypad 5 key
NUMPAD6 = 0x66  # Numeric keypad 6 key
NUMPAD7 = 0x67  # Numeric keypad 7 key
NUMPAD8 = 0x68  # Numeric keypad 8 key
NUMPAD9 = 0x69  # Numeric keypad 9 key
MULTIPLY = 0x6A  # Multiply key
ADD = 0x6B  # Add key
SEPARATOR = 0x6C  # Separator key
SUBTRACT = 0x6D  # Subtract key
DECIMAL = 0x6E  # Decimal key
DIVIDE = 0x6F  # Divide key
F1 = 0x70  # F1 key
F2 = 0x71  # F2 key
F3 = 0x72  # F3 key
F4 = 0x73  # F4 key
F5 = 0x74  # F5 key
F6 = 0x75  # F6 key
F7 = 0x76  # F7 key
F8 = 0x77  # F8 key
F9 = 0x78  # F9 key
F10 = 0x79  # F10 key
F11 = 0x7A  # F11 key
F12 = 0x7B  # F12 key
F13 = 0x7C  # F13 key
F14 = 0x7D  # F14 key
F15 = 0x7E  # F15 key
F16 = 0x7F  # F16 key
F17 = 0x80  # F17 key
F18 = 0x81  # F18 key
F19 = 0x82  # F19 key
F20 = 0x83  # F20 key
F21 = 0x84  # F21 key
F22 = 0x85  # F22 key
F23 = 0x86  # F23 key
F24 = 0x87  # F24 key
NUMLOCK = 0x90  # NUM LOCK key
SCROLL = 0x91  # SCROLL LOCK key
LSHIFT = 0xA0  # Left SHIFT key
RSHIFT = 0xA1  # Right SHIFT key
LCONTROL = 0xA2  # Left CONTROL key
RCONTROL = 0xA3  # Right CONTROL key
LMENU = 0xA4  # Left MENU key
RMENU = 0xA5  # Right MENU key
BROWSER_BACK = 0xA6  # Browser Back key
BROWSER_FORWARD = 0xA7  # Browser Forward key
BROWSER_REFRESH = 0xA8  # Browser Refresh key
BROWSER_STOP = 0xA9  # Browser Stop key
BROWSER_SEARCH = 0xAA  # Browser Search key
BROWSER_FAVORITES = 0xAB  # Browser Favorites key
BROWSER_HOME = 0xAC  # Browser Start and Home key
VOLUME_MUTE = 0xAD  # Volume Mute key
VOLUME_DOWN = 0xAE  # Volume Down key
VOLUME_UP = 0xAF  # Volume Up key
MEDIA_NEXT_TRACK = 0xB0  # Next Track key
MEDIA_PREV_TRACK = 0xB1  # Previous Track key
MEDIA_STOP = 0xB2  # Stop Media key
MEDIA_PLAY_PAUSE = 0xB3  # Play/Pause Media key
LAUNCH_MAIL = 0xB4  # Start Mail key
LAUNCH_MEDIA_SELECT = 0xB5  # Select Media key
LAUNCH_APP1 = 0xB6  # Start Application 1 key
LAUNCH_APP2 = 0xB7  # Start Application 2 key
OEM_1 = 0xBA  # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ';:' key
OEM_PLUS = 0xBB  # For any country/region, the '+' key
OEM_COMMA = 0xBC  # For any country/region, the ',' key
OEM_MINUS = 0xBD  # For any country/region, the '-' key
OEM_PERIOD = 0xBE  # For any country/region, the '.' key
OEM_2 = 0xBF  # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '/?' key =
OEM_3 = 0xC0  # Used for miscellaneous characters; it can vary by keyboard. = For the US standard keyboard, the '`~' key
OEM_4 = 0xDB  # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '[{' key
OEM_5 = 0xDC  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the '\|' key
OEM_6 = 0xDD  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the ']}' key
OEM_7 = 0xDE  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the 'single-quote/double-quote' key
OEM_8 = 0xDF  # Used for miscellaneous characters; it can vary by keyboard.
OEM_102 = 0xE2  # Either the angle bracket key or the backslash key on the RT 102-key keyboard 0xE3-E4 OEM specific
PROCESSKEY = 0xE5  # IME PROCESS key 0xE6 = OEM specific #
PACKET = 0xE7  # Used to pass Unicode characters as if they were keystrokes. The PACKET key is the low word of a 32-bit Virtual Key value used for non-keyboard input methods. For more information, see Remark in KEYBDINPUT, SendInput, WM_KEYDOWN, and WM_KEYUP #-
ATTN = 0xF6  # Attn key
CRSEL = 0xF7  # CrSel key
EXSEL = 0xF8  # ExSel key
EREOF = 0xF9  # Erase EOF key
PLAY = 0xFA  # Play key
ZOOM = 0xFB  # Zoom key
NONAME = 0xFC  # Reserved
PA1 = 0xFD  # PA1 key
OEM_CLEAR = 0xFE  #

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg", wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD),
                ("_input", _INPUT))


LPINPUT = ctypes.POINTER(INPUT)


def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT,  # nInputs
                             LPINPUT,  # pInputs
                             ctypes.c_int)  # cbSize


# Functions

def KeyDown(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def KeyUp(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def PressKey(hexKeyCode, duration=0):
    KeyDown(hexKeyCode)
    sleep(duration)
    KeyUp(hexKeyCode)


def MouseDown(hexKeyCode):
    x = INPUT(type=INPUT_MOUSE,
              mi=MOUSEINPUT(dwFlags=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def MouseUp(hexKeyCode):
    x = INPUT(type=INPUT_MOUSE,
              mi=MOUSEINPUT(dwFlags=hexKeyCode | 0x0004))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def ClickMouse(hexKeyCode, duration=0):
    MouseDown(hexKeyCode)
    sleep(duration)
    MouseUp(hexKeyCode)


def MoveMouseRelative(x, y):
    x = INPUT(type=INPUT_MOUSE,
              mi=MOUSEINPUT(dx=x, dy=y, dwFlags=0x0001))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


def MoveMouseAbsolute(x, y):
    # Get the screen dimensions
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    # Map absolute coordinates to the screen dimensions
    absolute_x = int(x * 65535 / screen_width)
    absolute_y = int(y * 65535 / screen_height)

    # Generate mouse input event for absolute movement
    x = INPUT(type=INPUT_MOUSE,
              mi=MOUSEINPUT(dx=absolute_x, dy=absolute_y,
                            dwFlags=0x8000 | 0x0001))  # 0x8000 indicates absolute movement
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
