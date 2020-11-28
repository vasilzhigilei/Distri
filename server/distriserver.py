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