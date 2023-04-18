import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class Handler(LoggingEventHandler):
 
    def __init__(self, podname, cmd):
        super().__init__()
        self.podname = podname
        self.cmd = cmd
 
    def on_any_event(self, event):
        if event.is_directory:
            return None
        
        os.system(f"kubectl cp {event.src_path} {self.podname}:/dev/")
            
        os.system(f"kubectl exec -it {self.podname} -- {self.cmd}")
 

if __name__ == "__main__":
    
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = Handler("pod", "ls -lt")
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()