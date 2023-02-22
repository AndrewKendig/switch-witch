from modules import window_manager, files_manager, settings, groups
import PySimpleGUI as sg
import webbrowser
import os
import shutil
# from PIL import Image

data_path = files_manager.init_data_folder(os)

window_manager.change_theme(sg, 'DarkGrey11')

window_object = window_manager.get_main_window_object(sg, os, data_path, files_manager)
window = window_manager.make_window(sg, window_object)

# mainloop
while True:
    event, values = window.read(timeout=500)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Settings':
        settings.show_settings_window(sg, window_manager)
    elif event == 'Groups':
        groups.show_groups_window(sg, os, window_manager, files_manager, data_path)
    elif event == 'Files':
        window_manager.show_not_implemented(sg, webbrowser)
    elif event == 'Select Group':
        versions_path = data_path + values['-GROUP-'] + '\\'
        versions = files_manager.get_versions(os, versions_path)
        window.Element('-VERSION-').Update(values=versions)

window.close()
