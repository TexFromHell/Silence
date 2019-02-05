from aiohttp import web
import socketio
import socket
import asyncio

# server.py

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


@sio.on('connect')
async def on_connection(sid, environ):
    print('----USER CONNECTED----')


@sio.on('get hostname')
async def get_hostname(sid, host):

    global hostname
    hostname = host

    global client_status
    client_status = 'True'

    print('HOSTNAME: "' + host + '" ID: "' + sid + '"')
    await sio.emit('ping status', client_status, room=sid)


@sio.on('get status')
async def get_status(sid, status):

    global received_status
    received_status = status

    try:
        print(hostname + ' : ' + received_status)

        await sio.emit('ping status', received_status, room=sid)

    except Exception as e:
        received_status = 'False'
        print(e)


@sio.on('disconnect')
async def on_disconnection(sid):

    global client_status
    client_status = 'False'

    print('----USER "' + hostname + '" DISCONNECTED----')
    print(hostname + ': ' + client_status)

web.run_app(app)



