from flask import Flask
from flask import render_template, url_for
from flask_socketio import SocketIO, emit
from pymixer import IconManager, AudioManager

host, port = "127.0.0.1", 5000

iconManager = IconManager()
audioManager = AudioManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True) # engineio_logger=True

def getProcessVolumes():
    processVolumes = {process[0]:process[2] for process in audioManager.getAllProcessInfo()}
    return processVolumes

def getProcessIcons():
    processIcons = {process[0]:iconManager.getIcon(process[0], process[1]) for process in audioManager.getAllProcessInfo()}
    return processIcons

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    processVolumes = getProcessVolumes()
    processIcons = getProcessIcons() 
    return render_template("pymixer.html", processVolumes=processVolumes, processIcons=processIcons)

@socketio.on("connected")
def connected(data):
    print("Connected", data)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('update')
def handle_update(data=None):
    if data:
        print(data)
        # update volume
        pass
    processVolumes = {process[0]:process[2] for process in audioManager.getAllProcessInfo()}
    socketio.emit("update", processVolumes)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)