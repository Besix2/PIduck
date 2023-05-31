import time
import json
import re
import random
import string
import os
import select
import inspect

constants = {}
variables = {}
functionsl = {}

with open("keycodes.json") as f:
    Keycodes = json.load(f)


def craft_packet(string, keycodes):
    special_keylist = (
        [
            "ENTER",
            "ESCAPE",
            "PAUSE BREAK",
            "PRINTSCREEN",
            "MENU APP",
            "F1",
            "F2",
            "F3",
            "F4",
            "F5",
            "F6",
            "F7",
            "F8",
            "F9",
            "F10",
            "F11",
            "F12",
        ]
        + [
            "UP",
            "DOWN",
            "LEFT",
            "RIGHT",
            "UPARROW",
            "DOWNARROW",
            "LEFTARROW",
            "RIGHTARROW",
            "PAGEUP",
            "PAGEDOWN",
            "HOME",
            "END",
            "INSERT",
            "DELETE",
            "DEL",
            "BACKSPACE",
            "TAB",
            "SPACE",
        ]
        + ["SHIFT", "ALT", "CONTROL", "CTRL", "COMMAND", "WINDOWS", "GUI"]
        + ["CAPSLOCK", "NUMLOCK", "SCROLLOCK"]
    )

    modifier = int("0x00", 16)
    if string in special_keylist:
        if isinstance(keycodes[string], list):
            keycode = int(keycodes[string][0], 16)
            modifier = int(keycodes[string][1], 16)

        else:
            keycode = int(keycodes[string], 16)
    elif string.isupper():
        modifier = int("0x02", 16)
        string = string.lower()
        keycode = int(keycodes[string], 16)
    else:
        if isinstance(keycodes[string], list):
            keycode = int(keycodes[string][0], 16)
            modifier = int(keycodes[string][1], 16)

        else:
            keycode = int(keycodes[string], 16)
    return bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00])


def check_variable(string):
    random_list = [
        "RANDOM_LOWERCASE_LETTER",
        "RANDOM_UPPERCASE_LETTER",
        "RANDOM_LETTER",
        "RANDOM_NUMBER",
        "RANDOM_SPECIAL",
        "RANDOM_CHAR",
    ]
    if len(string) > 1:
        for g in string.split(" "):
            if "(" or ")" in g:
                g = g.replace("(", "")
                g = g.replace(")", "")
            if g in variables:
            #     default_variables()
                string = string.replace(g, f"variables[{g!r}]")
            elif g in constants:
                string = string.replace(g, f"constants[{g}]")
            else:
                pass
    else:
        if string in variables:
            string = variables[string]
        if string in constants:
            string = constants[string]
    return string


def WRITE(string, keycodes):
    with open("/dev/hidg0", "wb") as f:
        string = check_variable(string)
        for char in string:
            packet = craft_packet(char, keycodes)
            f.write(packet)
            f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))


def STRINGLN(string, keycodes):
    with open("/dev/hidg0", "wb") as f:
        string = check_variable(string)
        for char in string:
            packet = craft_packet(char, keycodes)
            f.write(packet)
            f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        f.flush()
        time.sleep(0.1)
        f.write(bytes([0x00, 0x00, 0x28, 0x00, 0x00, 0x00, 0x00, 0x00]))
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))


def special_keys_write(string, keycodes):
    string_split = string.split()
    with open("/dev/hidg0", "wb") as f:
        if len(string_split) == 1:
            f.write(craft_packet(string, keycodes))
            f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        elif string == "GUI r" or string == "WINDOWS r":
            f.write(bytes([0x08, 0x00, 0x00, 0x15, 0x00, 0x00, 0x00, 0x00]))
            f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        else:
            mkeys = []
            nkeys = [0x04]
            for i in string_split:
                if isinstance(keycodes[i], list):
                    mkeys.append(int(keycodes[i][1], 16))
                else:
                    nkeys.append(int(keycodes[i], 16))

            if len(mkeys) > 1:
                modifiers = reduce(lambda x, y: x | y, mkeys)
            else:
                modifiers = mkeys[0]

            if len(nkeys) == 1:
                keycode = nkeys[0]
            else:
                keycode = []
                for key in nkeys:
                    keycode.append(key)
                    keycode.append(0x00)
                    keycode.pop()

            command = bytes([modifiers, 0x00, *keycode, 0x00, 0x00, 0x00, 0x00, 0x00])
            f.write(command)
            f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))


def DELAY(string):
    time.sleep(int(string) / 1000)


def DEFINE(constant, value):
    constants[constant] = value


def VAR(variable, value):  # only loop if something is part of variuables

    
    if "(" or ")" in value:
        value = value.replace("(", "")
        value = value.replace(")", "")
    for i in value.split(" "):
        if i in variables:
            value = value.replace(i, str(variables[i]))
        if i in constants:
            value = value.replace(i, str(constants[i]))
    if value.isdigit():
                if value.isnumeric():
                    value = int(value)
                else:
                    value = float(value)
    if type(value) == str:             
        if "+" in value or "-" in value or "*" in value or "/" in value:
            if "(" or ")" in value:
                value = value.replace("(", "")
                value = value.replace(")", "")
            value = eval(value)
        
    variables[variable] = value


def LOCK_KEYS_STATE(string):
    dev_file = os.open("/dev/hidg0", os.O_RDWR | os.O_NONBLOCK)

    while True:
        r, w, x = select.select([dev_file], [], [])
        if r:
            data = os.read(dev_file, 1)

            caps_lock_state = data[0] & 0x02

            if caps_lock_state:
                if string == "WAIT_FOR_CAPS_ON":
                    break
                if string == "WAIT_FOR_CAPS_CHANGE":
                    break
            else:
                if string == "WAIT_FOR_CAPS_OFF":
                    break
                if string == "WAIT_FOR_CAPS_CHANGE":
                    break

            num_lock_state = data[0] & 0x01

            if num_lock_state:
                if string == "WAIT_FOR_NUM_ON":
                    break
                if string == "WAIT_FOR_NUM_CHANGE":
                    break
            else:
                if string == "WAIT_FOR_NUM_OFF":
                    break
                if string == "WAIT_FOR_NUM_CHANGE":
                    break

            scroll_lock_state = data[0] & 0x04

            if scroll_lock_state:
                if string == "WAIT_FOR_SCROLL_ON":
                    break
                if string == "WAIT_FOR_SCROLL_CHANGE":
                    break
            else:
                if string == "WAIT_FOR_SCROLL_OFF":
                    break
                if string == "WAIT_FOR_SCROLL_CHANGE":
                    break


# def SAVE_RESTORE_LOCK_KEYS(option):
#     states = {}
#     if option == "save":
#         dev_file = os.open("/dev/hidg0", os.O_RDWR | os.O_NONBLOCK)
#         with open("/dev/hidg0", "wb") as f:  # pressing a lock key to get hid report
#             f.write(bytes([0x00, 0x00, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00]))
#             f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
#             f.write(bytes([0x00, 0x00, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00]))
#             f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
#         while True:
#             r, w, x = select.select([dev_file], [], [])
#             if r:
#                 data = os.read(dev_file, 1)
#                 caps_lock_state = data[0] & 0x02

#                 if caps_lock_state:
#                     states["CAPSLOCK"] = "on"
#                 else:
#                     states["CAPSLOCK"] = "off"

#                 num_lock_state = data[0] & 0x01

#                 if num_lock_state:
#                     states["NUMLOCK"] = "on"
#                 else:
#                     states["NUMLOCK"] = "off"

#                 scroll_lock_state = data[0] & 0x04

#                 if scroll_lock_state:
#                     states["SCROLLOCK"] = "on"
#                 else:
#                     states["SCROLLOCK"] = "off"
#                 break

#     if option == "restore":
#         dev_file = os.open("/dev/hidg0", os.O_RDWR | os.O_NONBLOCK)
#         with open("/dev/hidg0", "wb") as f:  # pressing a lock key to get hid report
#             f.write(bytes([0x00, 0x00, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00]))
#             f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
#             f.write(bytes([0x00, 0x00, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00]))
#             f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
#         while True:
#             r, w, x = select.select([dev_file], [], [])
#             if r:
#                 data = os.read(dev_file, 1)
#                 caps_lock_state = data[0] & 0x02

#                 if caps_lock_state:
#                     if states["CAPSLOCK"] == "off":
#                         special_keys_write("CAPSLOCK", Keycodes)
#                 else:
#                     if states["CAPSLOCK"] == "on":
#                         special_keys_write("CAPSLOCK", Keycodes)

#                 num_lock_state = data[0] & 0x01

#                 if num_lock_state:
#                     if states["NUMLOCK"] == "off":
#                         special_keys_write("NUMLOCK", Keycodes)
#                 else:
#                     if states["NUMLOCK"] == "on":
#                         special_keys_write("NUMLOCK", Keycodes)

#                 scroll_lock_state = data[0] & 0x04

#                 if scroll_lock_state:
#                     if states["SCROLLOCK"] == "off":
#                         special_keys_write("SCROLLOCK", Keycodes)
#                 else:
#                     if states["SCROLLOCK"] == "on":
#                         special_keys_write("SCROLLOCK", Keycodes)
#                 break


def CONDITIONS(condition):
    condition_split = condition.split("\n")
    i_condition = re.search(r"IF\s+(.*?)\s+THEN", condition_split[0]).group(1)
    for i in variables:
        if i in i_condition:
            i_condition = i_condition.replace(i, variables[i])
    for e in constants:
        if e in i_condition:
            i_condition = i_condition.replace(e, constants[e])
    if "||" in i_condition:
        i_condition = i_condition.replace("||", "or")
    if "$$" in i_condition:
        i_condition = i_condition.replace("||", "and")
    if "^" in i_condition:
        i_condition = i_condition.replace("||", "**")
    if "ELSE" in condition:
        if eval(i_condition):
            match = re.search(r"THEN\s+(.*?)\s+END_IF", condition, flags=re.DOTALL)
            if match:
                result = match.group(1)
                callf(e_result)
        else:
            for i in condition_split:
                if "ELSE" in i:
                    e_condition = re.search(
                        r"IF\s+(.*?)\s+THEN", condition_split[condition_split.index(i)]
                    ).group(1)
                    if eval(e_condition):
                        e_match = re.search(
                            r"THEN\s+(.*?)\s+END_IF", condition, flags=re.DOTALL
                        )
                        if e_match:
                            e_result = e_match.group(1)
                            callf(e_result)

    else:
        if eval(i_condition):
            match = re.search(r"THEN\s+(.*?)\s+END_IF", condition, flags=re.DOTALL)
            if match:
                result = match.group(1)
                callf(e_result)


def LOOPS(loop):
    loop_split = loop.split("\n")
    condition = loop_split[0].split("WHILE")[1].strip()
    condition = check_variable(condition)
    start_index = loop.find(loop_split[1])
    end_index = loop.find("END_WHILE")
    e_condition = loop[start_index:end_index]
    e_condition = e_condition.replace("\t","")
    while eval(condition):
        callf(e_condition)


def default_variables():
    VAR("RANDOM_LOWERCASE_LETTER", random.choice(string.ascii_lowercase))
    VAR("RANDOM_UPPERCASE_LETTER", random.choice(string.ascii_uppercase))
    VAR("RANDOM_LETTER", random.choice(string.ascii_letters))
    VAR("RANDOM_NUMBER", random.choice(string.digits))
    VAR("RANDOM_SPECIAL", random.choice(string.punctuation))
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digitsu
    punctuation = string.punctuation
    all_characters = lowercase_letters + uppercase_letters + digits + punctuation
    VAR("RANDOM_CHAR", random.choice(all_characters))
    if "$_RANDOM_MIN" in variables:
        VAR("$_RANDOM_INT", random.randrange(variables["$_RANDOM_MIN"], variables["$_RANDOM_MAX"]))

def FUNCTIONS(string):
    s_condition = string.split("\n")
    i_condition = s_condition[0].split()[1]
    condition_name = i_condition
    e_condition = string[string.index(s_condition[1]):string.index("END_FUNCTION")]
    e_condition = e_condition.strip()
    if "return" in string:
        function_string = f"def {i_condition}:\n\tcallf({e_condition}\n\treturn{functions[condition_name]})"
    else:
        function_string = f"callf(\"{e_condition}\")"
    functionsl[condition_name] = function_string


def HOLD_RELEASE(string, state):
    if state == "HOLD":
        f.write(craft_packet(string))
    if state == "RELEASE":
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))


def FUNCTION_CALL(function, script):
    exec(functionsl[function])

def callf(script):
    special_keylist = (
        [
            "ENTER",
            "ESCAPE",
            "PAUSE BREAK",
            "PRINTSCREEN",
            "MENU APP",
            "F1",
            "F2",
            "F3",
            "F4",
            "F5",
            "F6",
            "F7",
            "F8",
            "F9",
            "F10",
            "F11",
            "F12",
        ]
        + [
            "UP",
            "DOWN",
            "LEFT",
            "RIGHT",
            "UPARROW",
            "DOWNARROW",
            "LEFTARROW",
            "RIGHTARROW",
            "PAGEUP",
            "PAGEDOWN",
            "HOME",
            "END",
            "INSERT",
            "DELETE",
            "DEL",
            "BACKSPACE",
            "TAB",
            "SPACE",
        ]
        + ["SHIFT", "ALT", "CONTROL", "CTRL", "COMMAND", "WINDOWS", "GUI"]
        + ["CAPSLOCK", "NUMLOCK", "SCROLLOCK"]
    )
    lock_keys = [
        "WAIT_FOR_CAPS_ON",
        "WAIT_FOR_CAPS_OFF",
        "WAIT_FOR_CAPS_CHANGE",
        "WAIT_FOR_NUM_ON",
        "WAIT_FOR_NUM_OFF",
        "WAIT_FOR_NUM_CHANGE",
        "WAIT_FOR_SCROLL_ON",
        "WAIT_FOR_SCROLL_OFF",
        "WAIT_FOR_SCROLL_CHANGE",
    ]

    flag = True
    loopiterations = 0
    while flag:
        substrings = []
        for string in script.split("\n"):
            if string:
                substrings.append(string)
        if loopiterations == len(substrings):
            break        
        # del substrings[-1]
        for task in substrings:
            task_split = task.split()
            if task_split[0] == "DEFINE":
                DEFINE(task_split[1], " ".join(task_split[2:]))
            elif task_split[0] == "VAR":
                VAR(task_split[1], " ".join(task_split[3:]))
            elif task_split[0] == "DELAY":
                DELAY(task_split[1])
            elif task_split[0] == "STRING":
                WRITE(" ".join(task_split[1:]), Keycodes)
            elif task_split[0] == "STRINGLN":
                STRINGLN(" ".join(task_split[1:]), Keycodes)
            elif task_split[0] == "IF":
                sindex = script.find("IF")
                eindex = script.find("END_IF")
                extracted_condition = script[sindex : eindex + 6]
                script = script.replace(extracted_condition, "")
                CONDITIONS(extracted_condition)
            elif task_split[0] == "WHILE":
                sindex = script.find("WHILE")
                eindex = script.find("END_WHILE")
                extracted_condition = script[sindex : eindex + 9]
                script = script.replace(extracted_condition, "")
                LOOPS(extracted_condition)
                break
            elif task_split[0] == "INJECT_MOD":
                special_keys_write(task_split[1], Keycodes)
            elif task_split[0] == "STOP_PAYLOAD":
                exit()
            elif task_split[0] == "HOLD":
                HOLD_RELASE(task_split[1], "HOLD")
            elif task_split[0] == "FUNCTION":
                sindex = script.find("FUNCTION")
                eindex = script.find("END_FUNCTION")
                extracted_condition = script[sindex : eindex + 12]
                script = script.replace(extracted_condition, "")
                script = script[sindex:]
                FUNCTIONS(extracted_condition)
                loopiterations = 0
                break
            elif task_split[0] == "RETURN":
                caller_frame = inspect.currentframe().f_back
                caller_name = caller_frame.f_code.co_name
                return_value = check_variable(task_split[1])
                FUNCTIONS[caller_name] = return_value
            elif task_split[0] == "RELEASE":
                HOLD_RELASE(task_split[1], "RELEASE")
            elif task_split[0] in lock_keys:
                LOCK_KEYS_STATE(task_split[0])
            # elif task_split[0] == "SAVE_HOST_KEYBOARD_LOCK_STATE":
            #     SAVE_RESTORE_LOCK_KEYS("save")
            # elif task_split[0] == "RESTORE_HOST_KEYBOARD_LOCK_STATE":
            #     SAVE_RESTORE_LOCK_KEYS("restore")
            elif task_split[0] in variables:
                VAR(task_split[0], task[task.index("=") + 2:])
            elif task_split[0] in functionsl:
                FUNCTION_CALL(task_split[0], script)
            elif task_split[0] in special_keylist:
                special_keys_write(task, Keycodes)        
            else:
                flag = False
            loopiterations += 1   
with open("payload.txt", "r") as payload:
    callf(payload.read())
   
