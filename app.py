from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('template_connect')
def handle_template_connect(data):
    print('Template connected: ' + str(data["templateName"]))
    print(data)

@socketio.on('error')
def handle_error(data):
    print('received error: ' + data)

@app.route("/play_all")
def route_play_all():
    socketio.emit('play', broadcast=True)
    return "ok"

@app.route("/stop_all")
def route_stop_all():
    socketio.emit('stop', broadcast=True)
    return "ok"

if __name__ == '__main__':
    socketio.run(app)