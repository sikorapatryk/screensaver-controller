import mouse
import keyboard
import random
import time
from datetime import datetime, timedelta
from signal import signal, SIGINT
from sys import exit

period = timedelta(seconds=90)
next_time = datetime.now() + period

def init():
    print('działam jbc')
    global mouse_events
    mouse_events = []
    mouse.hook(mouse_events.append)

def handler(signal_received, frame):
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    mouse.unhook_all()
    exit(0)

signal(SIGINT, handler)
init()

while True:
    time.sleep(2)
    if len(mouse_events) > 0:
        next_time = datetime.now() + period
    else:
        if next_time <= datetime.now():
            keyboard.press_and_release('alt')
            next_time = datetime.now() + period
    mouse_events.clear()