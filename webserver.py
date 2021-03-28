from flask import Flask
from flask import render_template
from pymixer import IconManager, AudioManager



iconManager = IconManager()
audioManager = AudioManager()
app = Flask(__name__)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    processVolumes = {process[0]:process[2] for process in audioManager.getAllProcessInfo()}
    processIcons = {process[0]:iconManager.getIcon(process[0], process[1]) for process in audioManager.getAllProcessInfo()}
    return render_template("pymixer.html", processVolumes=processVolumes, processIcons=processIcons)

if __name__ == '__main__':
    app.run()