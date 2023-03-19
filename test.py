import time
import json


with open('keycodes.json') as f:
    Keycodes = json.load(f)

def STRING(string, keycodes):
    with open('/dev/hidg0', 'wb') as f:

        for char in string:
            if isinstance(keycodes[char], list):
                keycode = int(keycodes[char][0], 16)
                modifier = int(keycodes[char][1], 16)
            else:
                keycode = int(keycodes[char], 16)
                modifier = int("0x00", 16)

            f.write(bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00]))
            time.sleep(0.01)
            f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

def STRINGLN(string, keycodes):
    with open('/dev/hidg0', 'wb') as f:

        for char in string:
            if isinstance(keycodes[char], list):
                keycode = int(keycodes[char][0], 16)
                modifier = int(keycodes[char][1], 16)
            else:
                keycode = int(keycodes[char], 16)
                modifier = int("0x00", 16)

            f.write(bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00]))
            time.sleep(0.01)
            f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

        f.write(bytes([0x00, 0x00, 0x28, 0x00, 0x00, 0x00, 0x00, 0x00]))
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
def CURSORKEYS(string, keycodes):
    keylist = ["UP", "DOWN", "LEFT", "RIGHT", "UPARROW", "DOWNARROW", "LEFTARROW", "RIGHTARROW", "PAGEUP", "PAGEDOWN", "HOME", "END", "INSERT", "DELETE", "DEL", "BACKSPACE", "TAB", "SPACE"]
    for char in keylist:
        if char == string:
            if isinstance(keycodes[char], list):
                keycode = int(keycodes[char][0], 16)
                modifier = int(keycodes[char][1], 16)
            else:
                keycode = int(keycodes[char], 16)
                modifier = int("0x00", 16)
        else:
            continue
    with open('/dev/hidg0', 'wb') as f:
        f.write(bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00]))
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
def SYSTEMKEYS(string, keycodes):
    keylist = ["ENTER", "ESCAPE", "PAUSE BREAK", "PRINTSCREEN", "MENU APP", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
    for char in keylist:
        if char == string:
            keycode = int(keycodes[char], 16)
        else:
            continue
    with open('/dev/hidg0', 'wb') as f:
        f.write(bytes([0x00, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00]))
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

def MODIFIERKEYS(string, keycodes):
    keylist = ["SHIFT", "ALT", "CONTROL", "CTRL", "COMMAND", "WINDOWS", "GUI"]
    for char in keylist:
        if char == string:
            keycode = int(keycodes[char], 16)
        else:
            continue
    with open('/dev/hidg0', 'wb') as f:
        f.write(bytes([keycode, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

def LOCKKEYS(string, keycodes):
    keylist = ["CAPSLOCK", "NUMLOCK", "SCROLLOCK"]
    for char in keylist:
        if char == string:
            keycode = int(keycodes[char], 16)
        else:
            continue
    with open('/dev/hidg0', 'wb') as f:
        f.write(bytes([0x00, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00]))
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

def DELAY(string):
    time.sleep(int(string) / 10)
x = input("wahl: ")
time.sleep(1)
DELAY(x)

