from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, rooms, disconnect, emit
from os import path
from pathlib import Path
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

socket_clients = dict()
update_sets = dict()

config_path = path.join(Path.home(), ".casparcg_template_obs_bridge.json")

if path.exists(config_path):
    try:
        with open(config_path) as f:
            update_sets = json.load(f)
    except:
        update_sets = dict()

# SOCKETIO EVENTS
@socketio.on('template_connect')
def handle_template_connect(data):
    print('Template connected: ' + str(data["templateName"]))
    socket_clients[request.sid] = data
    emit('clients', socket_clients, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    if request.sid in socket_clients:
        del socket_clients[request.sid]
    print('Template disconnected: ' + str(request.sid))
    emit('clients', socket_clients, broadcast=True)

@socketio.on('request_clients')
def handle_connections():
    emit('clients', socket_clients)

@socketio.on('error')
def handle_error(data):
    print('received error: ' + data)

@socketio.on("template_play_all")
def handle_template_play_all():
    emit('play', broadcast=True, namespace="/")

@socketio.on("template_stop_all")
def handle_template_stop_all():
    emit('stop', broadcast=True, namespace="/")

@socketio.on("template_update_all")
def handle_template_update_all(data):
    emit('update', data, broadcast=True, namespace="/")

@socketio.on("template_play")
def handle_template_play(sid):
    emit("play", to=sid, namespace="/")

@socketio.on("template_stop")
def handle_template_stop(sid):
    emit("stop", to=sid, namespace="/")

@socketio.on("template_update")
def handle_template_update(sid, data):
    emit("update", data, to=sid, namespace="/")

@socketio.on("template_reload")
def handle_template_reload(sid):
    emit("reload", to=sid, namespace="/")

@socketio.on("template_delete")
def handle_template_delete(sid):
    request.sid = sid
    request.namespace = "/"
    disconnect()

@socketio.on("request_update_sets")
def handle_request_update_sets():
    emit("update_sets", update_sets, broadcast=True, namespace="/")

@socketio.on("add_update_set")
def handle_add_update_set(name, data):
    print(name, data)
    update_sets[name] = data
    emit("update_sets", update_sets, broadcast=True, namespace="/")

    with open(config_path, "w") as f:
        json.dump(update_sets, f)

@socketio.on("remove_update_set")
def handle_remove_update_set(name):
    print(name)
    del update_sets[name]
    emit("update_sets", update_sets, broadcast=True, namespace="/")

    with open(config_path, "w") as f:
        json.dump(update_sets, f)

# REST API
@app.route("/play_all", methods=['GET', 'POST'])
def route_play_all():
    emit('play', broadcast=True, namespace="/")
    return "ok"

@app.route("/stop_all", methods=['GET', 'POST'])
def route_stop_all():
    emit('stop', broadcast=True, namespace="/")
    return "ok"

@app.route("/update_all", methods=['POST'])
def route_update_all():
    emit('update', request.form, broadcast=True, namespace="/")
    return "ok"

@app.route("/<sid>/play", methods=['POST'])
def route_connection_play(sid):
    emit("play", to=sid, namespace="/")
    return "ok"

@app.route("/<sid>/stop", methods=['POST'])
def route_connection_stop(sid):
    emit("stop", to=sid, namespace="/")
    return "ok"

@app.route("/<sid>/update", methods=['POST'])
def route_connection_update(sid):
    emit("update", request.form, to=sid, namespace="/")
    return "ok"

@app.route("/<sid>/delete", methods=['POST'])
def route_connection_delete(sid):
    request.sid = sid
    request.namespace = "/"
    disconnect()
    return "ok"

@app.route("/")
def base():
    return send_from_directory(path.join('dashboard', 'public'), 'index.html')

@app.route("/inject.js")
def serve_inject():
    return send_from_directory(path.join('js_client_injected', 'dist'), 'main.js')

@app.route("/<path:path>")
def static_resources(path):
    return send_from_directory('dashboard/public', path)

if __name__ == '__main__':
    socketio.run(app)