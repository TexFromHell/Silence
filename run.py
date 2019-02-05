import main
from timeit import default_timer as timer
from pynput import keyboard
import socketio
import socket
import asyncio
import async_timeout


sio = socketio.Client()


def connect_to_server():

    global hostname
    hostname = socket.gethostname()

    try:
        sio.connect('http://0.0.0.0:8080')
        sio.emit('get hostname', hostname)

    except Exception as e:
        print('Client Error: ' + str(e))


connect_to_server()


@sio.on('ping status')
def ping_status(status):

    global conn_status
    conn_status = status

    try:

        print('connection status: ' + conn_status)
        sio.emit('get status', conn_status)
        sio.sleep(2)

    except EnvironmentError as e:

        print('Client Error: ' + str(e))
        conn_status = 'False'
        print('connection status: ' + conn_status)

        count = 0

        if conn_status == 'False':
            for i in range(20):
                count = count + 1
                print('attempting to connect...' + count)
                connect_to_server()
                sio.sleep(3)

        else:
            return


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

                global hostname
                global conn_status

                # main.authorization_screen()
                print(conn_status)
                main.authorization_screen(hostname, conn_status)
                listener.stop()

    # This statement executes the listen_for_combination function.
    with keyboard.Listener(on_press=listen_for_combination) as listener:
        listener.join()


run_gui()