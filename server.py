#
# ..................................................................
from typing import List, Any

from aiohttp import web
import socketio
import asyncio
import time


sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)

global users
users = []

# ..................................................................
@sio.on('connect')
async def on_connection(sid, environ):
    print('----USER CONNECTED----')
    print(sid)

    global user
    user = {
        'socket': sid,
        'status': 'True'
    }
    users.append(user)


# ..................................................................
@sio.on('get user')
async def on_user(sid, hostname):

    print(hostname)
    user.update({'name': hostname})


# ..................................................................
@sio.on('get data')
async def on_data(sid):

    await sio.emit('list client', users)
    await sio.sleep(2)


# ..................................................................
@sio.on('disconnect')
async def on_disconnection(sid):

    for i in users:
        if sid == i['socket']:
            users.remove(i)

    print('----USER DISCONNECTED----')
    print(sid)

web.run_app(app)



