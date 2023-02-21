from modules import window_manager
import PySimpleGUI as sg
import webbrowser
# import os
# import shutil
# from PIL import Image


window_manager.change_theme(sg, 'DarkGrey11')

# UI

window_object = window_manager.get_main_window_object(sg)
window = window_manager.start_window(sg, window_object)

# mainloop
while True:
    event, values = window.read(timeout=500)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Settings':
        window_manager.show_not_implemented(sg, webbrowser)
    elif event == 'Groups':
        window_manager.show_not_implemented(sg, webbrowser)
    elif event == 'Files':
        window_manager.show_not_implemented(sg, webbrowser)

window.close()
