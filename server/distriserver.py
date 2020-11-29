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
    rooms[newcode] = Room(newcode)
    rooms[newcode].dict['test'] = 123
    return newcode

@app.route('/r/<path:code>')
def room(code):
    # do room logic here
    # return html render if from browser
    # maybe return true bool for programatic connections to room
    return render_template('room.html', code=code, room=rooms[code].dict)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)

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
    code = data['code']
    key = data['key']
    value = data['value']
    rooms[code].dict[key] = value
    emit('updated data', {key:value}, room=code)

# ROOM CLASS
rooms = {}
class Room:
    def __init__(self, code):
        self.connections = 0
        self.dict = {}

if __name__ == '__main__':
    socketio.run(app)