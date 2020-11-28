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

rooms = {}

class Room:
    def __init__(self, code):
        self.code = code
        self.connections = 0
        self.dict = {}

if __name__ == '__main__':
    socketio.run(app)