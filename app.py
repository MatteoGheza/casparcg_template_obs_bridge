from flask import Flask, render_template, request, render_template
from flask_socketio import SocketIO, rooms, disconnect, emit
from nanoid import generate

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

socket_clients = dict()

@socketio.on('template_connect')
def handle_template_connect(data):
    print('Template connected: ' + str(data["templateName"]))
    if not "id" in data:
        template_id = generate()
        emit('new_template_id', template_id, namespace="/")
    else:
        template_id = data["id"]
        del data["id"]
    data["sid"] = request.sid
    socket_clients[template_id] = data

getSIDByTemplateID = lambda template_id: socket_clients[template_id]["sid"]
getTemplateIDBySID = lambda sid: next(filter(lambda template_id: socket_clients[template_id]["sid"] == sid, socket_clients.keys()))

@socketio.on('disconnect')
def disconnect():
    del socket_clients[getTemplateIDBySID(request.sid)]

@socketio.on('error')
def handle_error(data):
    print('received error: ' + data)

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

@app.route("/<template_id>/play", methods=['POST'])
def route_connection_play(template_id):
    emit("play", to=getSIDByTemplateID(template_id), namespace="/")
    return "ok"

@app.route("/<template_id>/stop", methods=['POST'])
def route_connection_stop(template_id):
    emit("stop", to=getSIDByTemplateID(template_id), namespace="/")
    return "ok"

@app.route("/<template_id>/update", methods=['POST'])
def route_connection_update(template_id):
    emit("update", request.form, to=template_id, namespace="/")
    return "ok"

@app.route("/<template_id>/delete", methods=['POST'])
def route_connection_delete(template_id):
    request.sid = getSIDByTemplateID(template_id)
    request.namespace = "/"
    disconnect()
    return "ok"

@app.route("/")
def route_index():
    print(socket_clients)
    return render_template("index.html", socket_clients=socket_clients)

if __name__ == '__main__':
    socketio.run(app)