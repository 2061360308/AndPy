import time
import threading

from application.terminal.terminalManager import TermManager
from application.interface.interface import start_server


if __name__ == '__main__':
    threading.Thread(target=TermManager.start_server).start()
    while True:
        time.sleep(0.1)