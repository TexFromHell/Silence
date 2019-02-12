#
# ..................................................................
from aiohttp import web
import socketio


sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


@sio.on('connect')
async def on_connection(sid, environ):

    global client_status
    client_status = 'True'

    print('----USER CONNECTED----')


@sio.on('get hostname')
async def get_hostname(sid, host):

    global hostname
    hostname = host

    print('HOSTNAME: "' + host + '" ID: "' + sid + '"')
    await sio.emit('ping status', client_status, room=sid)


@sio.on('get status')
async def get_status(sid, status):

    global client_status
    client_status = status

    try:
        print(hostname + ' : ' + status)
        await sio.emit('ping status', client_status, room=sid)

    except Exception as e:
        print(e)


@sio.on('disconnect')
async def on_disconnection(sid):

    global client_status
    client_status = 'False'

    print('----USER "' + hostname + '" DISCONNECTED----')

web.run_app(app)



