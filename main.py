from modules import menu, data
import PySimpleGUI as sg
import os
import shutil
from PIL import Image

if not os.path.isfile('settings.json'):
    data.save_data(settings=data.init_data('settings'))

settings = data.get_data('settings')

sg.theme(settings['general']['value']['style']['value'])

# UI
left_column = [[sg.Text(settings['general']['value']['style']['value'])]]
right_column = [[sg.Text('this is some text')]]

layout = [[menu.get_menu()],
          [sg.Column(left_column, element_justification='l'), sg.Column(right_column, element_justification='r')],
          [sg.Button('Bam', size=(8, 3), font='Corbel 20 bold')]]

window = sg.Window('Switch Witch', layout, size=(600, 500))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Settings':
        updated_settings = menu.show_settings(settings)
        if updated_settings:
            data.save_data(updated_settings)

window.close()
