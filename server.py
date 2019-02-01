from aiohttp import web
import socketio
import socket
import asyncio
from timeit import default_timer as timer

# server.py

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


@sio.on('connect')
async def on_connection(sid, environ):
    print('----USER CONNECTED----')
    

@sio.on('send hostname')
async def on_hostname(sid, host):

    print('Hostname: "' + host + '" Socket id: "' + sid + '"')

    global hostname
    hostname = host

    await sio.emit('get hostname', hostname, room=sid)


@sio.on('send status')
async def on_status(sid):

    global time
    time = timer()

    global status
    status = 'True'

    try:
        for i in range(int(time)):
            await sio.emit('get status', status, room=sid)
            print(hostname + ': ' + status)
            await sio.sleep(5)

    except Exception as e:
        print('Server Error: ' + str(e))


@sio.on('disconnect')
async def on_disconnection(sid):

    print('----USER "' + hostname + '" DISCONNECTED----')

    global status
    status = 'False'

    print(hostname + ': ' + status)


web.run_app(app)


