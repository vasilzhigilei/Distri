from flask import Flask
from flask import render_template
import secrets
app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD = True,
)

@app.route('/')
@app.route('/index')
def index():
    """
    Main page for frontend
    """
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
    return None

rooms = {}

class Room:
    def __init__(self, code):
        self.code = code
        self.dict = {}