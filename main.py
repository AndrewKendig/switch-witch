from modules import window_manager, files_manager, settings, groups, versions
import PySimpleGUI as sg
import webbrowser
import os
import shutil
# from PIL import Image

data_path = files_manager.init_data_folder(os)

group_folder = ''
version_folder = ''
output_folder = ''

window_manager.change_theme(sg, 'DarkBlue17')  # 'DarkPurple7'

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
        groups_list = files_manager.get_groups(os, data_path)
        window.Element('-GROUP-').Update(values=groups_list)
    elif event == 'Versions':
        versions.show_versions_window(sg, os, window_manager, files_manager, group_folder)
        versions_list = files_manager.get_versions(os, group_folder)
        window.Element('-VERSION-').Update(values=versions_list)
    elif event == 'Files':
        window_manager.show_not_implemented(sg, webbrowser)
    elif event == 'Select Group' and values['-GROUP-'] != '':
        group_folder = data_path + values['-GROUP-'] + '\\'
        output_folder = group_folder + 'Output\\'
        versions_list = files_manager.get_versions(os, group_folder)
        window.Element('-VERSION-').Update(values=versions_list)
    elif event == 'Switch to Version' and values['-VERSION-'] != '':
        version_folder = group_folder + 'Versions\\' + values['-VERSION-'] + '\\'
    elif event == 'Apply Changes':
        files_manager.push_files(shutil, version_folder, output_folder)

window.close()
