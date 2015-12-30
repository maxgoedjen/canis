from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    shutdown_server()
    return "Hello World!"

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
