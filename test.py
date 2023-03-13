import time
import json

# Load the keycodes from the json file
with open('keycodes.json') as f:
    keycodes = json.load(f)

# Open the hid device for writing
with open('/dev/hidg0', 'wb') as f:

    # Wait for 2 seconds before sending the first key
    time.sleep(2)

    # Get the string input from the user
    input_string = input("Enter a string: ")

    # Iterate through each character in the input string
    for char in input_string:

        # Get the corresponding HID keycode for the character
        keycode = int(keycodes[char], 16)

        # Send the HID keycode using f.write()
        f.write(bytes([0x00, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00]))

        # Wait for 0.1 seconds before sending the next key
        time.sleep(0.1)

    # Send a null character to release all the keys
        f.write(bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))

    # Wait for 2 seconds before exiting
    time.sleep(2)
