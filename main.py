from importlib.resources import path
import os
import sys
import time
import daemon
import logging
import re
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

dir = [a for a in os.listdir() if os.path.isdir(a)]
fecha = os.popen("date +%d").read()
file = [int(s) for s in re.findall(r'-?\d+\.?\d*', fecha)]

class testdaemon(daemon.Daemon):
    def run(self):
        if __name__ == "__main__":
                logging.basicConfig(filename=str(file[0]),level = logging.INFO , format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                logger = logging.getLogger()
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

daemon = testdaemon()

if 'start' == sys.argv[1]: 
    daemon.start()
elif 'stop' == sys.argv[1]: 
    daemon.stop()
elif 'restart' == sys.argv[1]: 
    daemon.restart()