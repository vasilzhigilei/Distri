from flask import Flask, request
from flask import render_template
from flask_socketio import SocketIO, emit, send, join_room, leave_room

from user_agents import parse
import secrets

# initialize Flask app
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True,
)

# initialize socketio
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

metadata = {'count':0,'browser':0,'python':0,'unknown':0}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', metadata=metadata)

@app.route('/api/generateroom')
def generateroom():
    """
    Generates a new room
    """
    room = secrets.token_urlsafe(4)
    ROOMS[room] = {}
    return room

@app.route('/r/<path:room>')
def room(room):
    # do room logic here
    # return html render if from browser
    # maybe return true bool for programatic connections to room
    return render_template('room.html', room=room)

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
    metadata['count'] += 1
    print(metadata)
    print('Connected client #' + str(metadata['count']) + ': ' + request.sid)

@socketio.on('disconnect')
def disconnect():
    print('Disconnected client #' + str(metadata['count']) + ': ' + request.sid)
    user_agent = parse(request.headers.get('User-Agent'))
    browser = user_agent.browser.family
    os = user_agent.os.family
    if browser == "Python Requests":
        metadata['python'] -= 1
    else:
        metadata['browser'] -= 1
    metadata['count'] -= 1

@socketio.on('JOIN')
def on_join(data):
    room = data['room']
    if room in ROOMS:
        join_room(room)
        emit('JOINED', ROOMS[room], room=request.sid) # send response with room dict back to client

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)

@socketio.on('SET')
def setvalue(data):
    room = data['room']
    key = data['key']
    value = data['value']
    ROOMS[room][key] = value #keyerror here if room doesn't exist
    emit('UPDATE', {key:value}, room=room)

# ROOM CLASS
ROOMS = {}
"""class Room:
    def __init__(self, code):
        self.connections = 0
        self.dict = {}"""

if __name__ == '__main__':
    socketio.run(app, debug=False)