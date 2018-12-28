import socketio
import socket

# standard Python
sio = socketio.Client()

local_name = socket.gethostname()
local_host = socket.gethostbyname(local_name)

global conn

conn = 'false'


def connect_client():
    sio.connect('http://0.0.0.0:8080')


@sio.on('connect')
def on_connect():
    conn = 'true'
    print('Client connected: ' + local_name + ' -', local_host)


@sio.on('response')
def client_response():
    data = {{
        conn, local_host, local_name}
    }
    sio.emit('response', data)


def disconnect_client():
    sio.disconnect()


@sio.on('disconnect')
def on_disconnect():
    print('Client disconnected: ' + local_name)

# fetch all remote functions from silent...

