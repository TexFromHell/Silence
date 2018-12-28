from aiohttp import web
import socketio

sio = socketio.AsyncServer(async_mode='aiohttp')
app = web.Application()
sio.attach(app)


@sio.on('disconnect')
def test_disconnect(sid):
    print('Client disconnected')


@sio.on('connect')
async def test_connect(sid, environ):
    await sio.emit('my response', {'data': 'Connected', 'count': 0}, room=sid,
                   namespace='/test')
    print('client connected')


@sio.on('response')
async def get_client_info(sid):

    print('client information: ')


web.run_app(app)
