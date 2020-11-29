from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
import secrets

# initialize Flask app
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True,
)

# initialize socketio
socketio = SocketIO(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/generateroom')
def generateroom():
    """
    Generates a new room
    """
    newcode = secrets.token_urlsafe(4)
    ROOMS[newcode] = {}
    ROOMS[newcode].dict['test'] = 123
    return newcode

@app.route('/r/<path:code>')
def room(room):
    # do room logic here
    # return html render if from browser
    # maybe return true bool for programatic connections to room
    return render_template('room.html', room=room)

@socketio.on('join')
def on_join(data):
    room = data['room']
    if room in ROOMS:
        join_room(room)
        emit('join response', ROOMS[room], room=request.sid) # send response with room dict back to client

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)

"""@socketio.on('get')
def getvalue(data):
    code = data['code']
    key = data['key']
    value = rooms[code].dict[key]
    emit('get response', value, room=request.sid)"""

@socketio.on('set')
def setvalue(data):
    room = data['room']
    key = data['key']
    value = data['value']
    ROOMS[room].dict[key] = value
    emit('updated data', {key:value}, room=room)

# ROOM CLASS
ROOMS = {}
"""class Room:
    def __init__(self, code):
        self.connections = 0
        self.dict = {}"""

if __name__ == '__main__':
    socketio.run(app)