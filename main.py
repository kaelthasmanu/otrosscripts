from importlib.resources import path
import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

dir = [a for a in os.listdir() if os.path.isdir(a)]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    observer = Observer()
    threads=[]
    for i in range(len(dir)):
            event_handler = LoggingEventHandler()
            observer.schedule(event_handler, dir[i], recursive=True)
            threads.append(observer)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
            observer.stop()
    observer.join()