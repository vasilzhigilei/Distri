from flask import Flask, request, flash, redirect, url_for, render_template
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from threading import Lock
from threading import Timer
from user_agents import parse
import secrets
import time
# initialize Flask app
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True,
)
app.secret_key = b'1'
thread = None
thread_lock = Lock() # thread starts at bottom of file
# initialize socketio
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

metadata = {'connections':0,'browser':0,'python':0,'unknown':0}

# note to self: add live every 5 second emit sitewide connections

def update_sitewide_stats():
    while(True):
        socketio.sleep(5) # every 5 seconds output sitewide stats
        socketio.emit('SITEWIDE_STATS', metadata) # broadcast


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', metadata=metadata, time=time.strftime('%I:%M:%S %p'))

@app.route('/api/generateroom')
def generateroom():
    """
    Generates a new room
    """
    room = secrets.token_urlsafe(4)
    ROOMS[room] = Room()
    return room

@app.route('/r/', defaults={'room': ''})
@app.route('/r/<path:room>')
def room(room):
    if room not in ROOMS:
        flash('Invalid room code')
        return redirect(url_for('index'))
    else:
        return render_template('room.html', room=room, metadata=metadata, time=time.strftime('%I:%M:%S %p'))

# Handler for a message recieved over 'connect' channel
@socketio.on('connect')
def connect():
    user_agent = parse(request.headers.get('User-Agent'))
    browser = user_agent.browser.family
    if browser == "Python Requests":
        metadata['python'] += 1
    else:
        metadata['browser'] += 1
        #in the future, add unknown, and do checks if really browser
        #print(user_agent.is_mobile, user_agent.is_pc, user_agent.is_bot)
    metadata['connections'] += 1
    print(metadata)
    print('Connected client #' + str(metadata['connections']) + ': ' + request.sid)
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=update_sitewide_stats)

@socketio.on('disconnect')
def disconnect():
    print('Disconnected client #' + str(metadata['connections']) + ': ' + request.sid)
    user_agent = parse(request.headers.get('User-Agent'))
    browser = user_agent.browser.family
    os = user_agent.os.family
    if browser == "Python Requests":
        metadata['python'] -= 1
    else:
        metadata['browser'] -= 1
    metadata['connections'] -= 1
    for room in ROOMS:
        if(request.sid in ROOMS[room].connected_users):
            ROOMS[room].connected_users.remove(request.sid)
            if request.sid in ROOMS[room].browser_users:
                ROOMS[room].browser_users.remove(request.sid)
            if request.sid in ROOMS[room].python_users:
                ROOMS[room].python_users.remove(request.sid)
            data = {'connections':len(ROOMS[room].connected_users),
                    'browser':len(ROOMS[room].browser_users),
                    'python':len(ROOMS[room].python_users)}
            emit('ROOM_STATS', data, room=room)

@socketio.on('JOIN')
def on_join(data):
    room = data['room']
    if room in ROOMS:
        join_room(room)
        emit('JOINED', ROOMS[room].data, room=request.sid) # send response with room dict back to client
        ROOMS[room].connected_users.append(request.sid)
        user_agent = parse(request.headers.get('User-Agent'))
        browser = user_agent.browser.family
        if browser == "Python Requests":
            ROOMS[room].python_users.append(request.sid)
        else:
            ROOMS[room].browser_users.append(request.sid)
        data = {'connections':len(ROOMS[room].connected_users),
                'browser':len(ROOMS[room].browser_users),
                'python':len(ROOMS[room].python_users)}
        emit('ROOM_STATS', data, room=room)

@socketio.on('leave')
def on_leave(data):
    """
    this method essentially never runs
    """
    room = data['room']
    leave_room(room)
    print(room, "LEAVE FIRED!!!!!!!")
    

@socketio.on('SET')
def setvalue(data):
    room = data['room']
    # if not in room do redirect here and disconnect client
    key = data['key']
    value = data['value']
    ROOMS[room].data[key] = value #keyerror here if room doesn't exist
    emit('UPDATE', {key:value}, room=room)

# ROOM CLASS
ROOMS = {}
class Room:
    def __init__(self):
        self.connected_users = []
        self.browser_users = []
        self.python_users = []
        self.data = {}

if __name__ == '__main__':
    socketio.run(app, debug=False)