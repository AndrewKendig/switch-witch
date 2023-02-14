from modules import menu, data
import PySimpleGUI as sg
import os
import shutil
from PIL import Image

if not os.path.isfile('settings.json'):
    data.save_data(settings=data.init_data('settings'))

settings = data.get_data('settings')

sg.theme(settings['general']['style'])

# UI
combo_style = {
    'size': (40, 1)
}
layout = [  [sg.Text('Pick the FIle or Folder')],
            [sg.Text(settings['general']['style']), sg.Button('Switch')],
            [sg.Button('Bam')]]

window = sg.Window('Switch Witch', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()
