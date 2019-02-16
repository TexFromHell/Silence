#
# ..................................................................
from aiohttp import web
import socketio

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
        'socket': sid
    }

    users.append(user)


# ..................................................................
@sio.on('get host')
async def on_user(sid, hostname):

    print(hostname)
    user.update({'name': hostname})


# ..................................................................
@sio.on('get client_list')
async def on_client_list(sid):

    await sio.emit('list client', users)
    await sio.sleep(1)


# ..................................................................
@sio.on('get client_data')
async def on_hey(sid, data):

    print('value: ' + data)

    client_data = [{
            'name': data,
            'status': 'True',
    }]

    await sio.emit('client data', client_data, room=sid)


# ..................................................................
@sio.on('disconnect')
async def on_disconnection(sid):

    for i in users:
        if sid == i['socket']:
            users.remove(i)

    print('----USER DISCONNECTED----')
    print(sid)

web.run_app(app)



