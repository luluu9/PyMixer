from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from time import sleep
from icoextract import IconExtractor, NoIconsAvailableError
import pathlib
import os

class IconManager:
    cwd = pathlib.Path(__file__).parent.absolute()
    def __init__(self):
        self.iconsDirPath = pathlib.Path(self.cwd / "static/")
        self.iconsAvailable = {}
        self.checkDir()
    

    ### Makes sure that directory for icons exists and gets previously used icons.
    def checkDir(self):
        if not os.path.isdir(self.iconsDirPath):
            os.makedirs(self.iconsDirPath)
        else:
            _, _, iconNames = next(os.walk(self.iconsDirPath))
            for iconName in iconNames:
                processName = str(pathlib.Path(iconName).with_suffix(""))
                self.iconsAvailable[processName] = iconName
    
    ### Extracts and returns a path to an icon. 
    ### If an icon doesn't exist, creates one. 
    ### If a process has no icon, returns None.
    def getIcon(self, processName, filepath):
        if not processName in self.iconsAvailable:
            try:
                iconName = processName + ".ico"
                iconPath = self.getIconPath(iconName)
                IconExtractor(filepath).export_icon(iconPath)
                self.iconsAvailable[processName] = iconName
            except NoIconsAvailableError:
                print("No icon for", processName)
                return None
        return self.iconsAvailable[processName]


    def getIconPath(self, iconName):
        return self.iconsDirPath / iconName


class AudioManager:
    def __init__(self):
        self.allProcessess = self.getAllProcesses()
    
    def getAllProcesses(self):
        processes = {}
        for session in AudioUtilities.GetAllSessions():
            if session.Process:
                processes[session.ProcessId] = session
        return processes

    def getSession(self, pid):
        if not pid in self.allProcessess:
            self.allProcessess = self.getAllProcesses()
            if not pid in self.allProcessess:
                return None
        return self.allProcessess[pid]
    
    def getProcessInfo(self, pid):
        session = self.getSession(pid)
        if session:
            process = session.Process
            if process:
                return {"pid": pid,
                        "name": process.name(), 
                        "filepath": process.exe(),
                        "volume": self.getVolume(pid)}

    def getAllProcessInfo(self):
        allProcessesInfo = []
        for pid in self.allProcessess:
            allProcessesInfo.append(self.getProcessInfo(pid))
        return allProcessesInfo

    def mute(self, pid):
        session = self.getSession(pid)
        if session:
            interface = session.SimpleAudioVolume
            interface.SetMute(1, None)
            print(pid, 'has been muted.')

    def unmute(self, pid):
        session = self.getSession(pid)
        if session:
            interface = session.SimpleAudioVolume
            interface.SetMute(0, None)
            print(pid, 'has been unmuted.')

    def getVolume(self, pid):
        session = self.getSession(pid)
        if session:
            interface = session.SimpleAudioVolume
            return interface.GetMasterVolume()

    def setVolume(self, pid, decibels):
        session = self.getSession(pid)
        if session:
            interface = session.SimpleAudioVolume
            # only set volume in the range 0.0 to 1.0
            self.volume = min(1.0, max(0.0, decibels))
            interface.SetMasterVolume(self.volume, None)


if __name__ == '__main__':
    iconManager = IconManager()
    audioManager = AudioManager()
    allProcesses = audioManager.getAllProcesses()
    for pid in allProcesses:
        print(audioManager.getVolume(pid))
        audioManager.setVolume(pid, 0.5)

# AUDIO:
# https://github.com/AndreMiras/pycaw
# ICONS:
# https://github.com/jlu5/icoextract/blob/master/icoextract/__init__.py
# https://github.com/firodj/extract-icon-py
# WEBSERVER:
# https://mrjoes.github.io/2013/06/21/python-realtime.html