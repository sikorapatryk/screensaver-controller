import PySimpleGUI as sg
from psgtray import SystemTray
from pystray import Icon as icon, Menu as menu, MenuItem as item
import ctypes
import _thread
from datetime import datetime, timedelta
import time
import mouse
import keyboard

state = False
running = True

def mouse_idle_disable(window, event, values):
    global running
    running = True

    period = timedelta(seconds=90)
    next_time = datetime.now() + period

    mouse_events = []
    mouse.hook(mouse_events.append)

    while running:
        time.sleep(2)
        if len(mouse_events) > 0:
            next_time = datetime.now() + period
        else:
            if next_time <= datetime.now():
                keyboard.press_and_release('caps_lock')
                keyboard.press_and_release('caps_lock')
                next_time = datetime.now() + period
        mouse_events.clear()
    
    mouse.unhook_all()

def main():

    menu = ['', ['!screensaver-controller | build 2008221122 | sikor.dev', '---','Show Window', '---', 'Exit']]
    tooltip = 'Double click to restore or right click and choose Show Window'
    iconb64 = b'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'

    frame_layout = [[sg.Checkbox('kernel display required', default=True, enable_events=True, key='kernel'), sg.Checkbox('mouse idle disable', default=True, enable_events=True, key='keyboard')]]

    layout = [[sg.Frame('options', frame_layout)],
              [sg.B('Hide Icon'), sg.B('Show Icon'), sg.B('Hide Window'), sg.Button('Exit')]]

    window = sg.Window('screensaver-controller', layout, finalize=True, enable_close_attempted_event=True, icon=iconb64)
    window.hide()

    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)          # default disable screensaver
    _thread.start_new_thread(mouse_idle_disable, (window, 'event', 'values'))   # default mouse idle disable

    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon=iconb64)
    tray.show_message('screensaver-controller', 'started!')

    while True:
        event, values = window.read()

        if event == tray.key:
            event = values[event]

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event in ('keyboard', 'kernel'):
            if event == 'kernel' and values['kernel']:
                ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
            elif event == 'kernel' and not values['kernel']:
                ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
            elif event == 'keyboard' and values['keyboard']:
                _thread.start_new_thread(mouse_idle_disable, (window, event, values))
            elif event == 'keyboard' and not values['keyboard']:
                global running
                running = False

        if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()
        elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()
        elif event == 'Hide Icon':
            tray.hide_icon()
        elif event == 'Show Icon':
            tray.show_icon()

    tray.close()
    window.close()

if __name__ == '__main__':
    main()
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)