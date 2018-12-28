import main
from pynput import keyboard
import server
import client


server.start_server()

# An variable for listen_for_combinations function to set the correct key combination to enter authorisation screen.
COMBINATIONS = [
    {keyboard.Key.shift_l}
]
# The currently active modifiers
current = set()


# This function listens for key combination in order to launch the interface of a program.
def listen_for_combination(combination):
    if any([combination in COMBO for COMBO in COMBINATIONS]):
        current.add(combination)

        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            main.authorization_screen()
            listener.stop()


# This statement executes the listen_for_combination function.
with keyboard.Listener(on_press=listen_for_combination) as listener:
    listener.join()

