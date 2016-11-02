#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

flag = 0

if async_mode is None:
    try:
        # monkey patching is necessary because this application uses a background
        # thread
        import eventlet
        async_mode = 'eventlet'
        eventlet.monkey_patch()
    except ImportError:
        pass

import serial
import sys
import subprocess
import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect

from vesaliusView import MetadataByZonegroup
 
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

ser = serial.Serial('/dev/ttyACM0', 9600)
prevNum = 0

thread = None


zonegroups = {
    0: '0',
    1:'66',
    2:'65',
    3:'69',
    4:'70',
    5:'71',
    6:'77',
    7:'67,68',
    8:'72,73',
    9:'75',
    10:'84',
    11:'86',
    12:'82,83',
    13:'80',
    14:'79',
    15:'78',
    16:'76',
    17: '948',
    18: '915,105,107,108',
    19: '82,83',
    20: '88',
    21: '104',
    22: '114,115,116',
    23: '81',
    24: '103',
    25: '89,90',
    26: '947',
    27: '949',
    28: '100',
    29: '101',
    30: '97',
    31: '99',
    32: '98',
    33: '954',
    34: '920,955,956,959',
    35: '953',
    36: '952',
    37: '952',
    38: '950',
    39: '919',
    40: '109',
    41: '920,955,956,959',
    42: '957,958',
    43: '957,958',
    44: '42',
    45: '961',
    46: '920,955,956,959',
    47: '964,965',
    48: '923,50,51',
    49: '121',
    50: '120',
    51: '117',
    52: '945',
    53: '962,966,967,968,969',
    54: '964,965',
    55: '946',
    56: '916,110,111,112,113',
    57: '923,50,51',
    58: '928,52',
    59: '928,52',
    60: '926',
    61: '962,966,967,968,969',
    62: '962,966,967,968,969',
    63: '962,966,967,968,969',
    64: '962,966,967,968,969',
    65: '38,937',
    66: '936',
    67: '57',
    68: '934,55',
    69: '931',
    70: '56',
    71: '53',
    72: '54'
    }




def background_thread1():
    count = 0
  
    while True:
        number = ser.readline()
        number = number.split('\r')
        number = number[0]

        try:
            number = int(number)
            if number != 0 and number != prevNum:
                
                zonegroup = zonegroups[number]
                socketio.emit('my response',
                     {'data': 'Server generated event', 'zonegroup': zonegroup},
                      namespace='/vesalius5')
            prevNum = number
        except ValueError:
            print ''
       
        
def background_thread2():
    '''"""Example of how to send server generated events to clients."""
    count = 0
    zonegroups = ('76', '76', '76', '76', '76', '76')
    time.sleep(1)
    while True:
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
        thread = Thread(target=background_thread1)
        thread.daemon = True
        thread.start()
    return render_template('main.html')


app.add_url_rule('/metadataByZonegroup/<string:zone_group>',
    view_func=MetadataByZonegroup.as_view('metadata_by_zonegroup'), methods=['GET'])



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
