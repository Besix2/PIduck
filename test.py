import time
import json

# Load the keycodes from the json file
with open('keycodes.json') as f:
    keycodes = json.load(f)

with open('/dev/hidg0', 'wb') as f:

    # Get the string input from the user
    input_string = input("Enter a string: ")

    # Iterate through each character in the input string
    for char in input_string:
        # if "_" value is a list, use the first element as the key code and the second as the modifier
        if isinstance(keycodes[char], list):

            keycode = int(keycodes[char][0], 16)
            modifier = int(keycodes[char][1], 16)
        else:
            # Get the corresponding HID keycode for the character
            keycode = int(keycodes[char], 16)
            modifier = int("0x00", 16)
        # Send the HID keycode using f.write()
        f.write(bytes([modifier, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00]))

        # Wait for 0.1 seconds before sending the next key
        time.sleep(0.01)

    # Send a null character to release all the keys
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

    # Wait for 2 seconds before exiting
    time.sleep(2)
