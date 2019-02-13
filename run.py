#
# ..................................................................
import main
from pynput import keyboard
import socketio
import socket


sio = socketio.Client()


# ..................................................................
def connect_client():
    global hostname
    hostname = socket.gethostname()

    sio.connect('http://0.0.0.0:8080')
    sio.emit('get data', hostname)


connect_client()


# ..................................................................
@sio.on('list client')
def list_client(users):

    global clients
    clients = users

    for client in clients:
        print(client['socket'])

    sio.emit('get data', hostname)


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

                main.authorization_screen(clients)
                listener.stop()

    with keyboard.Listener(on_press=listen_for_combination) as listener:
        listener.join()


run_gui()