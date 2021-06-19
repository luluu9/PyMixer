If you are using bluetooth speakers and you can't change volume, try this: https://www.dell.com/community/Inspiron/Can-t-control-volume-of-external-bluetooth-speakers-through/td-p/7496329
"You can change the value of “DisableAbsoluteVolume” manually into 1. (Path: HKLM\SYSTEM\ControlSet001\Control\Bluetooth\Audio\AVRCP\CT)"

TODO:
- change constant time updates to notification system: https://github.com/AndreMiras/pycaw/blob/develop/examples/volume_callback_example.py, https://github.com/AndreMiras/pycaw/issues/27 
- add option to change output device for apps: https://github.com/audiorouterdev/audio-router, https://github.com/File-New-Project/EarTrumpet, https://docs.microsoft.com/en-us/windows/win32/coreaudio/core-audio-apis-in-windows-vista, https://docs.microsoft.com/en-us/windows/win32/coreaudio/loopback-recording
"Although a client cannot change the session to which an existing stream is assigned, it can achieve a similar effect by deleting the stream (by releasing all references to it), creating a new stream to replace the deleted stream, and assigning the new stream to another session." https://docs.microsoft.com/en-us/windows/win32/coreaudio/audio-sessions 
https://github.com/joelspadin/AudioPipe + https://github.com/naudio/NAudio
do api for https://github.com/audiorouterdev/audio-router?
- app restart is necessary for update audio sessions
- audio session is hooked only from main output device