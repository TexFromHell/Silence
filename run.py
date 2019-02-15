#
# ..................................................................
import main
from pynput import keyboard
import socketio
import socket

sio = socketio.Client()
global hostname
hostname = socket.gethostname()

try:
    sio.connect('http://0.0.0.0:8080')
    sio.emit('get user', hostname)

except Exception as e:
    print(e)


# ..................................................................
def run_gui():

    combinations = [
        {keyboard.Key.shift_l}
    ]
    current = set()

    def listen_for_combination(combination):

        if any([combination in COMBO for COMBO in combinations]):
            current.add(combination)

            if any(all(k in current for k in COMBO) for COMBO in combinations):

                main.authorization_screen(sio)
                listener.stop()

    with keyboard.Listener(on_press=listen_for_combination) as listener:
        listener.join()


run_gui()