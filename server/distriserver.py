from flask import Flask
from flask import render_template
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
    # generate room here
    return "room url code here"

@app.route('r/<path:code>')
def room(code):
    # do room logic here
    # return html render if from browser
    # maybe return true bool for programatic connections to room
    return None