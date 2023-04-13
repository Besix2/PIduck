import time
import json
import re

constants = {}
variables = {}

with open('keycodes.json') as f:
    Keycodes = json.load(f)


def craft_packet(string, keycodes):
    if isinstance(keycodes[string], list):
        keycode = int(keycodes[string][0], 16)
        modifier = int(keycodes[string][1], 16)
    else:
        keycode = int(keycodes[string], 16)
        modifier = int("0x00", 16)
    return bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00])

def check_variable(char):
    if char in variables:
        char = variables[char]
    elif char in constants:
        char = constants[char]
    else:
        pass
    return char

def WRITE(string, keycodes):
    with open('/dev/hidg0', 'wb') as f:
        for j in string.split(" "):
            if j in variables:
                string = string.replace(j, check_variable[j])
            if j in constants:
                string = string.replace(j, constants[j])

        for char in string:
            packet = craft_packet(char, keycodes)
            f.write(packet)
            time.sleep(0.01)
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))


def STRINGLN(string, keycodes):
   with open('/dev/hidg0', 'wb') as f:
        for g in string.split(" "):
            if g in variables:
                string = string.replace(g, check_variable[g])
            if g in constants:
                string = string.replace(g, constants[g])

        for char in string:
            packet = craft_packet(char, keycodes)
            f.write(packet)
            time.sleep(0.01)
            print("1")
        f.write(bytes([0x00, 0x00, 0x28, 0x00, 0x00, 0x00, 0x00, 0x00]))
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
def special_keys_write(string, keycodes):
    print(string)
    string_split = string.split()
    with open('/dev/hidg0', 'wb') as f:
        if len(string_split) == 1:
             f.write(craft_packet(string, keycodes))
             f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        elif string == "GUI r" or string == "WINDOWS r":
            f.write(bytes([0x08, 0x00, 0x00, 0x15, 0x00, 0x00, 0x00, 0x00]))
            f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
            print("check 2")
        else:
            keys = []
            for i in string_split:
                keys.append(craft_packet(i, Keycodes))
            for key in keys:
                f.write(bytes(key))
            f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))


def DELAY(string):
    time.sleep(int(string) / 1000)


def DEFINE(constant, value):
    constants[constant] = value


def VAR(variable, value):  # use different splitting
    for i in value.split(" "):
        if i in variables:
            value = value.replace(i, variables[i])
        if i in constants:
            value = value.replace(i, constants[i])

    if len(value) > 1:
        value = eval(value)
    variables[variable] = value

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
        match = re.search(r'THEN\s+(.*?)\s+END_IF', condition, flags=re.DOTALL)
        if match:
            result = match.group(1)
            callf(result)

def callf(script):
    special_keylist = ["ENTER", "ESCAPE", "PAUSE BREAK", "PRINTSCREEN", "MENU APP", "F1", "F2", "F3", "F4", "F5", "F6",
                       "F7", "F8", "F9", "F10", "F11", "F12"] + \
                      ["UP", "DOWN", "LEFT", "RIGHT", "UPARROW", "DOWNARROW", "LEFTARROW", "RIGHTARROW", "PAGEUP",
                       "PAGEDOWN", "HOME", "END", "INSERT", "DELETE", "DEL", "BACKSPACE", "TAB", "SPACE"] + \
                      ["SHIFT", "ALT", "CONTROL", "CTRL", "COMMAND", "WINDOWS", "GUI"] + \
                      ["CAPSLOCK", "NUMLOCK", "SCROLLOCK"]
    print(repr(script))
    substrings = script.split('\n')
    print(substrings)
    del substrings[-1]
    for task in substrings:
        print(repr(task))
        task_split = task.split()
        if task_split[0] == "DEFINE":
            DEFINE(task_split[1], " ".join(task_split[2:]), Keycodes)
        if task_split[0] == "VAR":
            VAR(task_split[1], " ".join(task_split[3:]), Keycodes)
        if task_split[0] == "DELAY":
            DELAY(task_split[1])
        if task_split[0] == "STRING":
            WRITE(" ".join(task_split[1:]), Keycodes)
            print("check")
        if task_split[0] == "STRINGLN":
            STRINGLN(" ".join(task_split[1:]), Keycodes)
        for i in special_keylist:
            if i == task_split[0]:
                special_keys_write(task, Keycodes)
                print(task)
                print(i)

        if task_split[0] == "INJECT_MOD":
            special_keys_write(task_split[1], Keycodes)

with open("payload.txt", "r") as payload:
    callf(payload.read())
