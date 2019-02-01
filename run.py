import main
from pynput import keyboard
import socketio
import socket


sio = socketio.Client()


def connect_to_server():

    global hostname
    hostname = socket.gethostname()

    try:
        sio.connect('http://0.0.0.0:8080')
        sio.emit('send hostname', hostname)

    except Exception as e:
        print('Client Error: ' + str(e))


connect_to_server()


def collect_data():

    @sio.on('get hostname')
    def get_hostname(host):

        global user_name
        user_name = host

        print(user_name)

        sio.emit('send status')

    @sio.on('get status')
    def get_status(status):

        global conn_status
        conn_status = status

        print('connection: ' + conn_status)


collect_data()


def run_gui():
    # An variable for listen_for_combinations function to set the correct key combination to enter authorisation screen.

    combinations = [
        {keyboard.Key.shift_l}
    ]
    # The currently active modifiers
    current = set()

    # This function listens for key combination in order to launch the interface of a program.
    def listen_for_combination(combination):
        if any([combination in COMBO for COMBO in combinations]):
            current.add(combination)

            if any(all(k in current for k in COMBO) for COMBO in combinations):
                # main.authorization_screen()
                main.authorization_screen(user_name, conn_status)
                listener.stop()

    # This statement executes the listen_for_combination function.
    with keyboard.Listener(on_press=listen_for_combination) as listener:
        listener.join()


run_gui()