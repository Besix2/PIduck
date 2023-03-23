import time
import json
import re

constants = {}
variables = {}
flist = ["STRING ","STRINGLN ","CURSORKEYS","SYSTEMKEYS"]

with open('keycodes.json') as f:
    Keycodes = json.load(f)

def STRING(string, keycodes):
    print("check")
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

def DEFINE(constant, value):
    constants[constant] = value

def VAR(variable, value): #use different splitting
    variables[variable] = value

def MATH(equasion): #splitting in beetween parentheces at spaces
    split_equasion = equasion.split()
    for i in split_equasion:
        if "$" in i:
            split_equasion[split_equasion.index(i)] = str(variables[i])
        if "#" in i:
            split_equasion[split_equasion.index(i)] = str(constants[i])
        if i == "^":
            split_equasion[split_equasion.index(i)] = "**"
    converted_equation = " ".join(split_equasion)
    return converted_equation

def CONDITIONS(condition):
    e_condition = re.search(r'IF\s+(.*?)\s+THEN', condition).group(1)
    for i in variables:
        if i in e_condition:
            e_condition = e_condition.replace(i, variables[i])
    for e in constants:
        if e in e_condition:
            e_condition = e_condition.replace(e, constants[e])
    if "||" in e_condition:
        e_condition = e_condition.replace("||", "or")
    if "$$" in e_condition:
        e_condition = e_condition.replace("||", "and")
    if "^" in e_condition:
        e_condition = e_condition.replace("||", "**")
    if eval(e_condition):
        print("check1")
        match = re.search(r'THEN\s+(.*?)\s+END_IF', condition, flags=re.DOTALL)
        if match:
            result = match.group(1)
            substrings = result.split('\n')
            for function in flist:
                for substring in substrings:
                    if function in substring:
                        sindex = substrings.index(substring)
                        x = substrings[sindex]
                        x = x.replace(function,"")
                        if function == "STRING ":
                            STRING(x, Keycodes)

CONDITIONS("IF ( 200 - 200 == 0) THEN\nSTRING 42 is less than 1337\nSTRINGLN test\nSTRING test\nEND_IF")


