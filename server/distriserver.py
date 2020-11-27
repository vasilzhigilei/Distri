from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    """
    Main page for frontend
    """
    return 'Hello, World!'