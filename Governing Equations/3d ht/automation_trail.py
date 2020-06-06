from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import json

def folder(filename):
    file_name, file_extension = os.path.splitext(filename)
    if file_extension=='.png':folder='pngfiles'
    if file_extension=='.pdf':folder='pdffiles'
    if file_extension=='.lnk':folder='shortcut'
    else: pass
    new_name=folder_destination+'/'+folder+'/'+filename
    return new_name

class Myhandler(FileSystemEventHandler):
    i=1
    def on_modified(self,event):
        for filename in os.listdir(folder_to_track):
            src=folder_to_track+'/'+filename
            new_destination=folder(filename)
            os.rename(src,new_destination)

folder_to_track='C:/Users/usert/Desktop/f1'
folder_destination='C:/Users/usert/Desktop'
event_handler=Myhandler()
Observer=Observer()
Observer.schedule(event_handler,folder_to_track,recursive=True)
Observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    Observer.stop()
Observer.join()
