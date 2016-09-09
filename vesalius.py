#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        # monkey patching is necessary because this application uses a background
        # thread
        import eventlet
        async_mode = 'eventlet'
        eventlet.monkey_patch()
    except ImportError:
        pass

import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect

from vesaliusView import MetadataByZonegroup
 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

thread = None

def background_thread2():
    """Example of how to send server generated events to clients."""
    count = 0
    zonegroups = ('76', '76', '76', '76', '76', '76')
    time.sleep(1)
    '''while True:
        count += 1
        zonegroup = zonegroups[count%6]
        socketio.emit('my response',
                     {'data': 'Server generated event', 'zonegroup': zonegroup},
                      namespace='/vesalius5')
        time.sleep(10)'''

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread2)
        thread.daemon = True
        thread.start()
    return render_template('main.html')


app.add_url_rule('/metadataByZonegroup/<string:zone_group>',
    view_func=MetadataByZonegroup.as_view('metadata_by_zonegroup'), methods=['GET'])

#app.add_url_rule('/metadataByZoneid/<string:zone_id>',
#    view_func=MetadataByZoneid.as_view('metadata_by_zoneid'), methods=['GET'])


@socketio.on('connect', namespace='/vesalius5')
def test_connect():
    emit('my response connection', {'data': 'Connected', 'count': 0})

@socketio.on('zonegroup', namespace='/vesalius5')
def get_zonegroup(zonegroup):
    print "get zonegroup: ", zonegroup;


@socketio.on('disconnect', namespace='/vesalius5')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == "__main__":
    socketio.run(app, debug=True)
