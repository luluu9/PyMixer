from flask import Flask
from flask import render_template, url_for
from flask_socketio import SocketIO, emit
from pymixer import IconManager, AudioManager
from json import loads

host, port = "127.0.0.1", 5000

iconManager = IconManager()
audioManager = AudioManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True) # engineio_logger=True

def getProcessVolumes():
    processVolumes = {process["pid"]:process["volume"] for process in audioManager.getAllProcessInfo()}
    return processVolumes

def getProcessIcons():
    processIcons = {process["pid"]:iconManager.getIcon(process["name"], process["filepath"]) for process in audioManager.getAllProcessInfo()}
    return processIcons

def getBaseInfo():
    baseInfo = audioManager.getAllProcessInfo()
    for i in range(len(baseInfo)):
        process = baseInfo[i]
        baseInfo[i]["icon"] = iconManager.getIcon(process["name"], process["filepath"])
    return baseInfo


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    baseInfo = getBaseInfo()
    return render_template("pymixer.html", baseInfo=baseInfo)

@socketio.on("connected")
def connected(data):
    print("Connected", data)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('update')
def handle_update(data=None):
    if data:
        values = loads(data)
        for pid, volume in values.items():
            audioManager.setVolume(int(pid), int(volume)/100.0)
    processVolumes = {process["pid"]:process["volume"] for process in audioManager.getAllProcessInfo()}
    socketio.emit("update", processVolumes)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)